/*
 * worker.js: receives "Report a problem" submissions and files each one as an issue
 * in the private GitHub repository bpacini-alt/textbook-feedback.
 *
 * Shared by both books. The source lives in feedback/worker.js in each textbook
 * repository, and the two copies must stay identical.
 *
 * Cloudflare runs this only for /api/* (see run_worker_first in wrangler.jsonc).
 * Every other request goes straight to the static site.
 *
 * Needs one secret on each Worker, set in the Cloudflare dashboard (never in this repo):
 *   GITHUB_TOKEN  a fine-grained GitHub token with Issues: Read and write on textbook-feedback only
 */

const REPO = 'bpacini-alt/textbook-feedback';
const MAX_BODY = 20000;  // bytes; a real report is far smaller
const LIMITS = { book: 60, chapter: 200, section: 200, type: 60, details: 4000, quote: 600, contact: 200, page: 500, device: 500 };

function json(status, data) {
  return new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
}

function clean(value, max) {
  return String(value == null ? '' : value).replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '').trim().slice(0, max);
}

// Student text goes into a quote block. "@" gets an invisible joiner so a report can't notify GitHub users.
function quote(s) {
  return s ? s.replace(/@/g, '@⁠').split(/\r?\n/).map(line => '> ' + line).join('\n') : '> (none)';
}

function cell(s) {
  return (s || '—').replace(/@/g, '@⁠').replace(/\|/g, '\\|').replace(/\r?\n/g, ' ');
}

function chapterLabel(chapter) {
  const m = chapter.match(/^\s*(?:Chapter\s*)?(\d+)\b/i);
  return m ? 'Ch. ' + m[1] : chapter.slice(0, 40);
}

export function makeIssue(r) {
  const summary = r.details.split(/\s+/).slice(0, 12).join(' ');
  const title = `[${r.book || 'Textbook'}] ${chapterLabel(r.chapter)} · ${r.type || 'Report'}: ${summary}${r.details.split(/\s+/).length > 12 ? '…' : ''}`.slice(0, 200);
  const body = [
    '| | |',
    '|---|---|',
    `| **Book** | ${cell(r.book)} |`,
    `| **Chapter** | ${cell(r.chapter)} |`,
    `| **Section** | ${cell(r.section)} |`,
    `| **Type** | ${cell(r.type)} |`,
    `| **Page** | ${cell(r.page)} |`,
    `| **Device** | ${cell(r.device)} |`,
    `| **Contact** | ${cell(r.contact || 'not given')} |`,
    '',
    '### What the reader said',
    quote(r.details),
    '',
    '### Text they highlighted',
    quote(r.quote),
    '',
    '<sub>Filed by the Report a problem button.</sub>',
  ].join('\n');
  return { title: title.replace(/@/g, '@\u2060'), body };
}

export async function handleReport(request, env) {
  if (request.method !== 'POST') return json(405, { error: 'method' });
  const origin = request.headers.get('Origin');
  if (origin && origin !== new URL(request.url).origin) return json(403, { error: 'origin' });
  if (!env.GITHUB_TOKEN) return json(503, { error: 'not_configured' });

  const raw = await request.text();
  if (raw.length > MAX_BODY) return json(413, { error: 'too_large' });
  let data;
  try { data = JSON.parse(raw); } catch { return json(400, { error: 'bad_json' }); }
  if (!data || typeof data !== 'object') return json(400, { error: 'bad_json' });

  // The form's hidden "website" field is empty for people and filled in by most bots. Pretend it worked.
  if (data.website) return json(200, { ok: true });

  const r = {};
  for (const [key, max] of Object.entries(LIMITS)) r[key] = clean(data[key], max);
  if (r.details.length < 3) return json(400, { error: 'details' });

  const issue = makeIssue(r);
  const gh = await fetch(`${env.GITHUB_API || 'https://api.github.com'}/repos/${REPO}/issues`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.GITHUB_TOKEN}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'textbook-report-button',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(issue),
  });
  if (!gh.ok) {
    console.log('GitHub issue failed', gh.status, (await gh.text()).slice(0, 300));
    return json(502, { error: 'github' });
  }
  const made = await gh.json();
  return json(200, { ok: true, number: made.number });
}


const RATINGS_SCHEMA = [
  'CREATE TABLE IF NOT EXISTS reading_ratings (',
  '  id INTEGER PRIMARY KEY AUTOINCREMENT,',
  '  book TEXT NOT NULL,',
  '  reading_id TEXT NOT NULL,',
  '  semester TEXT NOT NULL,',
  '  rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 4),',
  '  client_id TEXT NOT NULL,',
  '  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,',
  '  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,',
  '  UNIQUE (book, reading_id, semester, client_id)',
  ');',
  'CREATE INDEX IF NOT EXISTS idx_reading_ratings_lookup ON reading_ratings (book, reading_id, semester);',
].join('\n');

const RATING_BOOKS = new Set(['econ-150', 'science-of-learning']);

function ratingJson(status, data, clientId) {
  const headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-store',
  };
  if (clientId) {
    headers['Set-Cookie'] = 'bb_client=' + encodeURIComponent(clientId) + '; Max-Age=31536000; Path=/; SameSite=Lax; Secure; HttpOnly';
  }
  return new Response(JSON.stringify(data), { status, headers });
}

function getCookie(request, name) {
  const header = request.headers.get('Cookie') || '';
  const item = header.split(';').map(part => part.trim()).find(part => part.startsWith(name + '='));
  return item ? decodeURIComponent(item.slice(name.length + 1)) : '';
}

function semesterKey(env) {
  if (env.RATINGS_SEMESTER) return clean(env.RATINGS_SEMESTER, 60);
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Denver',
    year: 'numeric',
    month: 'numeric',
  }).formatToParts(new Date());
  const year = parts.find(part => part.type === 'year').value;
  const month = Number(parts.find(part => part.type === 'month').value);
  const term = month <= 4 ? 'Winter' : month <= 7 ? 'Spring' : 'Fall';
  return term + ' ' + year;
}

function validRatingTarget(book, reading) {
  return RATING_BOOKS.has(book) && /^[a-z0-9][a-z0-9-]{0,80}$/.test(reading);
}

async function ratingSummary(db, book, reading, semester, clientId) {
  const results = await db.batch([
    db.prepare('SELECT rating, COUNT(*) AS count FROM reading_ratings WHERE book = ? AND reading_id = ? AND semester = ? GROUP BY rating').bind(book, reading, semester),
    db.prepare('SELECT rating FROM reading_ratings WHERE book = ? AND reading_id = ? AND semester = ? AND client_id = ? LIMIT 1').bind(book, reading, semester, clientId),
  ]);
  const counts = { 1: 0, 2: 0, 3: 0, 4: 0 };
  for (const row of results[0].results || []) counts[Number(row.rating)] = Number(row.count);
  const total = Object.values(counts).reduce((sum, count) => sum + count, 0);
  const percentages = {};
  for (const rating of [1, 2, 3, 4]) {
    percentages[rating] = total ? Math.round((counts[rating] / total) * 1000) / 10 : 0;
  }
  const mine = results[1].results && results[1].results[0];
  return {
    ok: true, book, reading, semester, counts, total, percentages,
    yourRating: mine ? Number(mine.rating) : null,
  };
}

async function handleRatings(request, env) {
  try {
  if (!['GET', 'POST'].includes(request.method)) return ratingJson(405, { error: 'method' });
  const origin = request.headers.get('Origin');
  if (origin && origin !== new URL(request.url).origin) return ratingJson(403, { error: 'origin' });
  if (!env.RATINGS_DB) return ratingJson(503, { error: 'ratings_not_configured' });

  const url = new URL(request.url);
  let book = clean(url.searchParams.get('book'), 60);
  let reading = clean(url.searchParams.get('reading'), 100);
  let rating = null;

  if (request.method === 'POST') {
    const raw = await request.text();
    if (raw.length > 2000) return ratingJson(413, { error: 'too_large' });
    let data;
    try { data = JSON.parse(raw); } catch { return ratingJson(400, { error: 'bad_json' }); }
    book = clean(data && data.book, 60);
    reading = clean(data && data.reading, 100);
    rating = Number(data && data.rating);
  }

  if (!validRatingTarget(book, reading)) return ratingJson(400, { error: 'bad_target' });
  if (request.method === 'POST' && (!Number.isInteger(rating) || rating < 1 || rating > 4)) {
    return ratingJson(400, { error: 'bad_rating' });
  }

  const clientId = getCookie(request, 'bb_client') || crypto.randomUUID();
  const semester = semesterKey(env);
  await env.RATINGS_DB.prepare(
    'CREATE TABLE IF NOT EXISTS reading_ratings (' +
    'id INTEGER PRIMARY KEY AUTOINCREMENT,' +
    'book TEXT NOT NULL,' +
    'reading_id TEXT NOT NULL,' +
    'semester TEXT NOT NULL,' +
    'rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 4),' +
    'client_id TEXT NOT NULL,' +
    'created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,' +
    'updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,' +
    'UNIQUE (book, reading_id, semester, client_id)' +
    ')'
  ).run();
  await env.RATINGS_DB.prepare(
    'CREATE INDEX IF NOT EXISTS idx_reading_ratings_lookup ON reading_ratings (book, reading_id, semester)'
  ).run();

  if (request.method === 'POST') {
    await env.RATINGS_DB.batch([
      env.RATINGS_DB.prepare(
        'DELETE FROM reading_ratings WHERE book = ? AND reading_id = ? AND semester = ? AND client_id = ?'
      ).bind(book, reading, semester, clientId),
      env.RATINGS_DB.prepare(
        'INSERT INTO reading_ratings (book, reading_id, semester, rating, client_id) VALUES (?, ?, ?, ?, ?)'
      ).bind(book, reading, semester, rating, clientId),
    ]);
  }

  return ratingJson(200, await ratingSummary(env.RATINGS_DB, book, reading, semester, clientId), clientId);  } catch (error) {
    return ratingJson(500, {
      error: 'ratings_database_error',
      message: error instanceof Error ? error.message : String(error),
    });
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/report') return handleReport(request, env);
    if (url.pathname === '/api/ratings') return handleRatings(request, env);
    if (url.pathname.startsWith('/api/')) return json(404, { error: 'not_found' });
    return env.ASSETS.fetch(request);
  },
};
