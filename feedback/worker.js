/*
 * worker.js: receives "Report a problem" submissions and files each one as an issue
 * in the private GitHub repository bpacini-alt/textbook-feedback.
 *
 * Shared by both books. The source lives in feedback/worker.js in each textbook
 * repository, and the two copies must stay identical.
 *
 * Cloudflare runs this for /api/*, /editor, and /editor/* (see run_worker_first in wrangler.jsonc).
 * Feedback, ratings, and author editing run here; other requests go to the static site.
 *
 * Configure these in Cloudflare, never in this repo:
 *   GITHUB_TOKEN         Issues access to textbook-feedback
 *   EDITOR_GITHUB_TOKEN  Contents read/write on this textbook repository
 *   ACCESS_TEAM_DOMAIN, ACCESS_AUD, EDITOR_EMAILS  editor authorization settings
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

async function ratingMine(db, book, semester, clientId) {
  const rows = await db.prepare(
    'SELECT reading_id, rating FROM reading_ratings WHERE book = ? AND semester = ? AND client_id = ?'
  ).bind(book, semester, clientId).all();
  const ratings = {};
  for (const row of rows.results || []) ratings[row.reading_id] = Number(row.rating);
  return { ok: true, book, semester, ratings };
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
async function ratingSummaries(db, book, semester, clientId) {
  const results = await db.batch([
    db.prepare('SELECT reading_id, rating, COUNT(*) AS count FROM reading_ratings WHERE book = ? AND semester = ? GROUP BY reading_id, rating').bind(book, semester),
    db.prepare('SELECT reading_id, rating FROM reading_ratings WHERE book = ? AND semester = ? AND client_id = ?').bind(book, semester, clientId),
  ]);
  const summaries = {};
  for (const row of results[0].results || []) {
    const id = row.reading_id;
    if (!summaries[id]) summaries[id] = { counts: { 1: 0, 2: 0, 3: 0, 4: 0 } };
    summaries[id].counts[Number(row.rating)] = Number(row.count);
  }
  const yourRatings = {};
  for (const row of results[1].results || []) yourRatings[row.reading_id] = Number(row.rating);
  for (const [reading, summary] of Object.entries(summaries)) {
    const total = Object.values(summary.counts).reduce((sum, count) => sum + count, 0);
    const percentages = {};
    for (const rating of [1, 2, 3, 4]) {
      percentages[rating] = total ? Math.round((summary.counts[rating] / total) * 1000) / 10 : 0;
    }
    summaries[reading] = {
      ok: true, book, reading, semester, counts: summary.counts, total, percentages,
      yourRating: yourRatings[reading] || null,
    };
  }
  return { ok: true, book, semester, summaries };
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
  const mineRequest = request.method === 'GET' && url.searchParams.get('mine') === '1';
  const allRequest = request.method === 'GET' && url.searchParams.get('all') === '1';

  if (request.method === 'POST') {
    const raw = await request.text();
    if (raw.length > 2000) return ratingJson(413, { error: 'too_large' });
    let data;
    try { data = JSON.parse(raw); } catch { return ratingJson(400, { error: 'bad_json' }); }
    book = clean(data && data.book, 60);
    reading = clean(data && data.reading, 100);
    rating = Number(data && data.rating);
  }

  if (mineRequest || allRequest) {
    if (!RATING_BOOKS.has(book)) return ratingJson(400, { error: 'bad_target' });
  } else if (!validRatingTarget(book, reading)) return ratingJson(400, { error: 'bad_target' });
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

  if (allRequest) return ratingJson(200, await ratingSummaries(env.RATINGS_DB, book, semester, clientId), clientId);
  if (mineRequest) return ratingJson(200, await ratingMine(env.RATINGS_DB, book, semester, clientId), clientId);

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


const EDITOR_BOOKS = {
  'econ-150': { repo: 'bpacini-alt/Econ-150-textbook', generated: false },
  'science-of-learning': { repo: 'bpacini-alt/edcor-310-textbook', generated: true },
};
let editorSigningKeys = null;
let editorSigningKeysExpire = 0;

function decodeBase64Url(value) {
  const normalized = value.replace(/-/g, '+').replace(/_/g, '/');
  const padded = normalized + '='.repeat((4 - normalized.length % 4) % 4);
  const binary = atob(padded);
  return Uint8Array.from(binary, c => c.charCodeAt(0));
}
function decodeTokenPart(value) {
  return JSON.parse(new TextDecoder().decode(decodeBase64Url(value)));
}
async function verifyEditorIdentity(request, env) {
  const teamDomain = String(env.ACCESS_TEAM_DOMAIN || '').replace(/\/+$/, '');
  const audience = String(env.ACCESS_AUD || '').trim();
  if (!teamDomain || !audience) return { ok: false, status: 503, error: 'editor_access_not_configured' };
  const token = request.headers.get('Cf-Access-Jwt-Assertion') || '';
  const parts = token.split('.');
  if (parts.length !== 3) return { ok: false, status: 401, error: 'access_token_missing' };
  try {
    const header = decodeTokenPart(parts[0]);
    const payload = decodeTokenPart(parts[1]);
    if (header.alg !== 'RS256' || !header.kid || payload.iss !== teamDomain) {
      return { ok: false, status: 403, error: 'access_token_invalid' };
    }
    const audiences = Array.isArray(payload.aud) ? payload.aud : [payload.aud];
    const now = Math.floor(Date.now() / 1000);
    if (!audiences.includes(audience) || !Number.isFinite(payload.exp) || payload.exp <= now ||
        (Number.isFinite(payload.nbf) && payload.nbf > now)) {
      return { ok: false, status: 403, error: 'access_token_invalid' };
    }
    if (!editorSigningKeys || editorSigningKeysExpire < Date.now()) {
      const response = await fetch(teamDomain + '/cdn-cgi/access/certs');
      if (!response.ok) throw new Error('access_keys_unavailable');
      const keySet = await response.json();
      editorSigningKeys = keySet.keys || [];
      editorSigningKeysExpire = Date.now() + 15 * 60 * 1000;
    }
    const jwk = editorSigningKeys.find(key => key.kid === header.kid);
    if (!jwk) return { ok: false, status: 403, error: 'access_token_invalid' };
    const key = await crypto.subtle.importKey(
      'jwk', jwk, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']
    );
    const valid = await crypto.subtle.verify(
      'RSASSA-PKCS1-v1_5', key, decodeBase64Url(parts[2]), new TextEncoder().encode(parts[0] + '.' + parts[1])
    );
    const email = String(payload.email || '').trim().toLowerCase();
    const allowedEmails = String(env.EDITOR_EMAILS || '').split(',').map(value => value.trim().toLowerCase()).filter(Boolean);
    if (!valid || !allowedEmails.includes(email)) return { ok: false, status: 403, error: 'editor_forbidden' };
    return { ok: true, email: email };
  } catch (error) {
    return { ok: false, status: 403, error: error instanceof Error ? error.message : 'access_token_invalid' };
  }
}
function editorGitHubHeaders(env) {
  return {
    'Authorization': 'Bearer ' + env.EDITOR_GITHUB_TOKEN,
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'textbook-prose-editor',
    'Content-Type': 'application/json',
  };
}
async function editorGitHub(env, repo, path, options) {
  const base = env.GITHUB_API || 'https://api.github.com';
  const response = await fetch(base + '/repos/' + repo + '/' + path, {
    ...(options || {}), headers: editorGitHubHeaders(env),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error('github_' + response.status + (data.message ? '_' + clean(data.message, 100) : ''));
  return data;
}
function decodeGitHubFile(value) {
  const compact = String(value || '').replace(/\s/g, '');
  const binary = atob(compact);
  const bytes = Uint8Array.from(binary, c => c.charCodeAt(0));
  return new TextDecoder().decode(bytes);
}
async function editorReadFile(env, book, path, ref) {
  const config = EDITOR_BOOKS[book];
  const targetRef = encodeURIComponent(ref || 'main');
  const result = await editorGitHub(env, config.repo, 'contents/' + path + '?ref=' + targetRef);
  return { content: decodeGitHubFile(result.content), sha: result.sha };
}
async function editorTarget(env, book, path) {
  const config = EDITOR_BOOKS[book];
  if (!config || !/^etb-live\/[^/]+\.html$/.test(path) || path.includes('..')) return null;
  const manifestFile = await editorReadFile(env, book, 'etb-live/manifest.json');
  const manifest = JSON.parse(manifestFile.content);
  const filename = path.slice('etb-live/'.length);
  const entry = (manifest.chapters || []).find(item => item.file === filename);
  if (!entry) return null;
  return { config: config, filename: filename, title: entry.title || filename };
}
async function editorReadPage(env, book, target, path) {
  const head = await editorGitHub(env, target.config.repo, 'git/ref/heads/main');
  const headSha = head.object.sha;
  const source = await editorReadFile(env, book, path, headSha);
  if (!source.content.trim()) throw new Error('page_empty');
  const live = target.config.generated
    ? await editorReadFile(env, book, 'site/' + target.filename, headSha)
    : source;
  return { book: book, path: path, title: target.title, headSha: headSha, source: source.content, sourceSha: source.sha, live: live.content, liveSha: live.sha };
}
async function editorCommitFiles(env, repo, files, message, expectedHeadSha) {
  const ref = await editorGitHub(env, repo, 'git/ref/heads/main');
  const parentSha = ref.object.sha;
  if (parentSha !== expectedHeadSha) throw new Error('page_changed_elsewhere');
  const parent = await editorGitHub(env, repo, 'git/commits/' + parentSha);
  const blobs = await Promise.all(files.map(file => editorGitHub(env, repo, 'git/blobs', {
    method: 'POST', body: JSON.stringify({ content: file.content, encoding: 'utf-8' }),
  })));
  const tree = await editorGitHub(env, repo, 'git/trees', {
    method: 'POST',
    body: JSON.stringify({
      base_tree: parent.tree.sha,
      tree: files.map((file, index) => ({
        path: file.path, mode: '100644', type: 'blob', sha: blobs[index].sha,
      })),
    }),
  });
  const commit = await editorGitHub(env, repo, 'git/commits', {
    method: 'POST',
    body: JSON.stringify({ message: message, tree: tree.sha, parents: [parentSha] }),
  });
  const base = env.GITHUB_API || 'https://api.github.com';
  const response = await fetch(base + '/repos/' + repo + '/git/refs/heads/main', {
    method: 'PATCH',
    headers: editorGitHubHeaders(env),
    body: JSON.stringify({ sha: commit.sha, force: false }),
  });
  if (!response.ok) {
    if (response.status === 422) throw new Error('page_changed_elsewhere');
    throw new Error('github_publish_' + response.status);
  }
  return commit.sha;
}
async function handleEditorApi(request, env) {
  const identity = await verifyEditorIdentity(request, env);
  if (!identity.ok) return json(identity.status, { error: identity.error });
  if (!env.EDITOR_GITHUB_TOKEN) return json(503, { error: 'editor_github_not_configured' });
  const url = new URL(request.url);
  if (request.method === 'GET') {
    const book = clean(url.searchParams.get('book'), 60);
    const path = clean(url.searchParams.get('path'), 200);
    const target = await editorTarget(env, book, path);
    if (!target) return json(404, { error: 'page_not_found' });
    try {
      return json(200, await editorReadPage(env, book, target, path));
    } catch (error) {
      return json(502, { error: error instanceof Error ? error.message : 'github_read_failed' });
    }
  }
  if (request.method !== 'POST') return json(405, { error: 'method' });
  const origin = request.headers.get('Origin');
  if (!origin || origin !== url.origin) return json(403, { error: 'origin' });
  if (!String(request.headers.get('Content-Type') || '').toLowerCase().startsWith('application/json')) {
    return json(415, { error: 'content_type' });
  }
  const raw = await request.text();
  if (raw.length > 3000000) return json(413, { error: 'too_large' });
  let data;
  try { data = JSON.parse(raw); } catch { return json(400, { error: 'bad_json' }); }
  const book = clean(data && data.book, 60);
  const path = clean(data && data.path, 200);
  const target = await editorTarget(env, book, path);
  if (!target || typeof data.sourceContent !== 'string' || typeof data.liveContent !== 'string') {
    return json(400, { error: 'bad_target' });
  }
  try {
    const current = await editorReadPage(env, book, target, path);
    if (current.headSha !== data.headSha || current.sourceSha !== data.sourceSha || current.liveSha !== data.liveSha) {
      return json(409, { error: 'page_changed_elsewhere' });
    }
    const files = [{ path: path, content: data.sourceContent }];
    if (target.config.generated) files.push({ path: 'site/' + target.filename, content: data.liveContent });
    const commitSha = await editorCommitFiles(env, target.config.repo, files, 'Edit ' + target.title + ' from textbook editor', current.headSha);
    const updated = await editorReadPage(env, book, target, path);
    return json(200, { ok: true, commit: commitSha, headSha: updated.headSha, sourceSha: updated.sourceSha, liveSha: updated.liveSha });
  } catch (error) {
    const message = error instanceof Error ? error.message : 'publish_failed';
    if (message === 'page_changed_elsewhere') return json(409, { error: message });
    return json(502, { error: message });
  }
}


export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/report') return handleReport(request, env);
    if (url.pathname === '/api/ratings') return handleRatings(request, env);
    if (url.pathname === '/editor/api') return handleEditorApi(request, env);
    if (url.pathname === '/editor' || url.pathname.startsWith('/editor/')) {
      const identity = await verifyEditorIdentity(request, env);
      if (!identity.ok) return json(identity.status, { error: identity.error });
      if (url.pathname === '/editor/api') return handleEditorApi(request, env);
      return env.ASSETS.fetch(request);
    }
    if (url.pathname.startsWith('/api/')) return json(404, { error: 'not_found' });
    return env.ASSETS.fetch(request);
  },
};
