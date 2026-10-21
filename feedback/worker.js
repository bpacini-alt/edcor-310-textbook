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

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/report') return handleReport(request, env);
    if (url.pathname.startsWith('/api/')) return json(404, { error: 'not_found' });
    return env.ASSETS.fetch(request);
  },
};
