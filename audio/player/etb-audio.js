/*
 * ETB audio player. Shared by every chapter. See audio/README.md.
 *
 * Adds a Listen button to the chapter's title card, a Listen link on each
 * section label, a docked player, and a text-only reading view.
 *
 * Two voices:
 *   - If the page has <script type="application/json" id="etb-audio-data">
 *     listing recorded MP3s, it plays those.
 *   - Otherwise it reads the chapter aloud with the device's built-in voice,
 *     highlighting each sentence as it goes. Nothing to generate or host.
 *
 * Author controls on any element in a chapter:
 *   data-narrate="skip"             leave it out of the audio and text-only view
 *   data-narrate-text="Say this"    read this instead of what's on the page
 */
(function () {
  'use strict';
  var root = document.querySelector('.etb');
  if (!root || root.getAttribute('data-audio-ready')) return;

  /* Which voice? Recorded MP3s if this chapter has them, otherwise the device's own voice. */
  var dataEl = document.getElementById('etb-audio-data');
  var D = null;
  try { D = dataEl ? JSON.parse(dataEl.textContent) : null; } catch (e) { D = null; }
  var FILES = !!(D && D.sections && D.sections.length);
  var synth = window.speechSynthesis;
  var TTS = !FILES && !!(synth && window.SpeechSynthesisUtterance);
  if (!FILES && !TTS) return;
  root.setAttribute('data-audio-ready', '1');

  /* ================= Settings: what gets read aloud ================= */
  var WPM = 155;
  var CUE = 'Pause and try answering on your own before you go on.';
  var DRILL_GAP = 4; /* seconds of quiet after a quick drill question */
  var SKIP = ['etb-flipgrid', 'etb-alsoknow', 'etb-yt', 'etb-yt-hr', 'etb-learnmore', 'etb-title-watermark',
    'etb-title-meta', 'etb-title-unit', 'etb-exam', 'etb-frq', 'etb-ap', 'etb-title-listen', 'etb-listen-here', 'etb-rv'];
  var CHIPS = ['etb-ret-badge', 'etb-ret-arrow', 'etb-check-tag', 'etb-check-arrow', 'etb-practice-badge',
    'etb-practice-arrow', 'etb-reveal-arrow'];
  var LABELS = ['etb-app-badge', 'etb-app-title', 'etb-syn-header', 'etb-note-label', 'etb-worked-badge',
    'etb-worked-title', 'etb-recap-eyebrow', 'etb-recap-title', 'etb-ledger-eyebrow', 'etb-ledger-title', 'etb-synth-eyebrow'];
  /* Blocks after the concepts that get their own place in the contents: [class, label, title element, header for the Listen link] */
  var MAJOR = [
    ['etb-applications', 'In the classroom', '.etb-app-title', '.etb-app-header'],
    ['etb-synthesis', 'Wrap-up', '.etb-syn-header', '.etb-syn-header'],
    ['etb-synth', 'Synthesis', null, null],
    ['etb-recap', 'The story so far', '.etb-recap-title', null],
    ['etb-ledger', 'Running ledger', '.etb-ledger-title', null]
  ];
  var SKIP_TAG = /^(SCRIPT|STYLE|IMG|PICTURE|IFRAME|VIDEO|AUDIO|CANVAS|SVG|INPUT|BUTTON|SELECT|TEXTAREA|HR|NOSCRIPT|TEMPLATE)$/;
  var INLINE_TAG = /^(STRONG|EM|B|I|A|CITE|SUP|SUB|CODE|ABBR|MARK|U|SMALL|Q|BR|TIME|DFN|S|SPAN|KBD|VAR|DATA)$/;
  var BLOCK_SEL = 'div,p,ul,ol,li,table,h1,h2,h3,h4,h5,h6,blockquote,details,section,figure';

  /* ================= Helpers ================= */
  function has(el, list) { if (!el || !el.classList) return false; for (var i = 0; i < list.length; i++) if (el.classList.contains(list[i])) return true; return false; }
  function skipEl(el, extra) {
    return SKIP_TAG.test(el.tagName.toUpperCase()) || has(el, SKIP) || (extra && has(el, extra)) ||
      el.getAttribute('data-narrate') === 'skip' || el.getAttribute('aria-hidden') === 'true';
  }
  function inlineEl(el) {
    var t = el.tagName.toUpperCase();
    if (!INLINE_TAG.test(t) || has(el, LABELS) || el.hasAttribute('data-narrate-text')) return false;
    return t !== 'SPAN' || !el.querySelector(BLOCK_SEL);
  }
  function collect(el, out, extra) {
    for (var c = el.firstChild; c; c = c.nextSibling) {
      if (c.nodeType === 3) out.push(c);
      else if (c.nodeType === 1 && !skipEl(c, extra)) { if (c.tagName === 'BR') out.push(null); else collect(c, out, extra); }
    }
  }
  function squish(s) { return (s || '').replace(/ /g, ' ').replace(/\s+/g, ' ').trim(); }
  function textOf(el, extra) { var n = []; collect(el, n, extra); return squish(n.map(function (x) { return x ? x.nodeValue : ' '; }).join('')); }
  function sentence(s) { s = squish(s); return s && !/[.!?:"”’)]$/.test(s) ? s + '.' : s; }
  function speakable(s) {
    return squish(s).replace(/[►▼▲▸▾↓↑]/g, '').replace(/\s&\s|&/g, ' and ').replace(/~\s?(\d)/g, 'about $1')
      .replace(/\s→\s/g, ', so ').replace(/\s?÷\s?/g, ' divided by ').replace(/\s?×\s?/g, ' times ')
      .replace(/\s?=\s?/g, ' equals ').replace(/(^|[\s(\[])[−-](?=\d)/g, '$1minus ').replace(/(^|[\s(\[])\+(?=\d)/g, '$1plus ')
      .replace(/(\d|\))\s[−-]\s(?=[\d(])/g, '$1 minus ').replace(/\s+/g, ' ').trim();
  }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function fmt(t) { t = Math.max(0, Math.round(t || 0)); var h = Math.floor(t / 3600), m = Math.floor(t % 3600 / 60), s = t % 60; return (h ? h + ':' + (m < 10 ? '0' : '') : '') + m + ':' + (s < 10 ? '0' : '') + s; }
  function mins(t) { return Math.max(1, Math.round(t / 60)) + ' min'; }
  function store(k, v) { try { if (v === undefined) { var x = localStorage.getItem(k); return x ? JSON.parse(x) : null; } localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }
  function now() { return (window.performance && performance.now) ? performance.now() : Date.now(); }

  /* ================= Pull the readable text out of the chapter ================= */
  var blocks = [], units = [], secs = [];
  var seg = (window.Intl && Intl.Segmenter) ? new Intl.Segmenter('en', { granularity: 'sentence' }) : null;

  function splitSentences(s) {
    var out = [];
    if (seg) { var it = seg.segment(s)[Symbol.iterator](), r; while (!(r = it.next()).done) out.push([r.value.index, r.value.index + r.value.segment.length]); return out; }
    var re = /[^.!?]+(?:[.!?]+["”’)]*\s*|$)/g, m;
    while ((m = re.exec(s)) && m[0]) out.push([m.index, m.index + m[0].length]);
    return out;
  }
  /* Some browsers stop speaking partway through a long utterance, so long sentences are spoken in pieces. */
  function pieces(text) {
    if (text.length <= 180) return [text];
    var bits = text.replace(/([,;:—–])\s+/g, '$1\u0001').split('\u0001'), out = [], cur = '';
    bits.forEach(function (b) {
      while (b.length > 180) { var cut = b.lastIndexOf(' ', 160); if (cut < 40) cut = 160; if (cur) { out.push(cur); cur = ''; } out.push(b.slice(0, cut)); b = b.slice(cut + 1); }
      if (cur && (cur + ' ' + b).length > 180) { out.push(cur); cur = b; } else cur = cur ? cur + ' ' + b : b;
    });
    if (cur) out.push(cur);
    return out;
  }
  function addUnit(sec, block, text, range, hl, gap) {
    text = speakable(text);
    if (!text) return;
    gap = gap || 0;
    units.push({ sec: sec, block: block, text: text, parts: pieces(text), range: range, el: hl, gap: gap, dur: text.split(' ').length / WPM * 60 + 0.35 + gap });
  }
  function locate(map, pos) {
    for (var i = map.length - 1; i >= 0; i--) if (map[i].at <= pos) return [map[i].n, Math.min(pos - map[i].at, map[i].n.nodeValue.length)];
    return [map[0].n, 0];
  }
  function addBlock(nodes, sec, kind) {
    var str = '', map = [];
    nodes.forEach(function (n) { if (!n) { str += ' '; return; } map.push({ n: n, at: str.length }); str += n.nodeValue; });
    if (!map.length || !/\S/.test(str)) return;
    var host = map[0].n.parentElement;
    var hl = host ? host.closest(BLOCK_SEL) : null;
    var b = blocks.push({ sec: sec, kind: kind, text: squish(str) }) - 1;
    splitSentences(str).forEach(function (r) {
      var a = r[0], z = r[1];
      while (a < z && /\s/.test(str[a])) a++;
      while (z > a && /\s/.test(str[z - 1])) z--;
      if (z <= a) return;
      var rg = null;
      try { rg = document.createRange(); var s = locate(map, a), e = locate(map, z); rg.setStart(s[0], s[1]); rg.setEnd(e[0], e[1]); } catch (x) { rg = null; }
      addUnit(sec, b, str.slice(a, z), rg, hl);
    });
  }
  function said(sec, kind, speech, hl, readText, gap) {
    var b = blocks.push({ sec: sec, kind: kind, text: readText == null ? speech : readText, el: hl }) - 1;
    addUnit(sec, b, speech, null, hl, gap);
  }
  function walk(node, sec) {
    var buf = [];
    function flush() { if (buf.length) addBlock(buf, sec, 'p'); buf = []; }
    for (var c = node.firstChild; c; c = c.nextSibling) {
      if (c.nodeType === 3) { buf.push(c); continue; }
      if (c.nodeType !== 1 || skipEl(c)) continue;
      if (c.tagName === 'BR') { buf.push(null); continue; }
      if (inlineEl(c)) { collect(c, buf); continue; }
      flush();
      handle(c, sec);
    }
    flush();
  }
  function table(tb, sec) {
    var head = [].map.call(tb.querySelectorAll('thead th'), function (h) { return textOf(h); });
    var rows = [].slice.call(tb.querySelectorAll('tbody tr'));
    if (!rows.length) {
      rows = [].slice.call(tb.querySelectorAll('tr'));
      if (!head.length && rows[0] && rows[0].querySelector('th')) head = [].map.call(rows.shift().children, function (h) { return textOf(h); });
    }
    rows.forEach(function (tr) {
      var cells = [].map.call(tr.children, function (td) { return textOf(td); });
      if (!cells.join('')) return;
      var parts = [sentence(cells[0])];
      for (var i = 1; i < cells.length; i++) if (cells[i]) parts.push(sentence(head[i] ? head[i] + ': ' + cells[i] : cells[i]));
      said(sec, 'row', parts.join(' '), tr);
    });
  }
  function handle(c, sec) {
    var t = c.tagName.toUpperCase();
    if (c.hasAttribute('data-narrate-text')) { said(sec, 'p', c.getAttribute('data-narrate-text'), c); return; }
    if (c.classList.contains('etb-slbl')) {
      var nx = c.nextElementSibling, l = textOf(c);
      if (l && nx && !skipEl(nx)) said(sec, 'label', sentence(l.replace(/\s·\s/g, ': ')), c, l);
      return;
    }
    if (has(c, LABELS)) { var lt = textOf(c); if (lt) said(sec, 'minor', sentence(lt.replace(/\s·\s/g, ': ')), c, lt); return; }
    if (t === 'DETAILS') {
      var sm = c.querySelector('summary');
      if (!sm) return;
      var badge = sm.querySelector('.etb-ret-badge,.etb-check-tag,.etb-practice-badge');
      var q = textOf(sm, CHIPS);
      if (!q) return;
      var bt = badge ? squish(badge.textContent) : 'Question';
      /* Retrieval practice gets a spoken cue. Quick drills get a few seconds of quiet instead. */
      if (c.classList.contains('etb-retrieval')) said(sec, 'prompt', sentence(bt) + ' ' + sentence(q) + ' ' + CUE, sm, bt + ': ' + q);
      else said(sec, 'prompt', sentence(bt) + ' ' + sentence(q), sm, bt + ': ' + q, DRILL_GAP);
      return;
    }
    if (t === 'TABLE') { table(c, sec); return; }
    if (c.classList.contains('etb-figure')) {
      var cap = c.querySelector('.etb-figure-cap,figcaption'), ct = cap ? textOf(cap) : '';
      if (ct) said(sec, 'minor', sentence(ct), c, ct);
      return;
    }
    if (/^H[1-6]$/.test(t)) { var hn = []; collect(c, hn); addBlock(hn, sec, 'heading'); return; }
    walk(c, sec);
  }

  /* Sections: the opening, each major concept, and the closing blocks */
  var card = root.querySelector('.etb-title-card');
  var num = squish((root.querySelector('.etb-title-watermark') || {}).textContent);
  var titleEl = card && (card.querySelector('.etb-title-main') || card.querySelector('h1,h2'));
  var subEl = card && card.querySelector('.etb-title-sub');
  var chapTitle = titleEl ? squish(titleEl.textContent) : squish(document.title);
  function newSec(id, title, label, anchor) { secs.push({ id: id, title: title, label: label, els: [], anchor: anchor }); return secs.length - 1; }

  var cs = newSec('intro', chapTitle, 'Introduction', null), k = 0;
  if (num) said(cs, 'chapter', 'Chapter ' + num + '.', titleEl, '');
  if (titleEl) { var tn = []; collect(titleEl, tn); addBlock(tn, cs, 'title'); }
  if (subEl) { var sn = []; collect(subEl, sn); addBlock(sn, cs, 'subtitle'); }
  [].forEach.call(root.children, function (c) {
    if (c === card || skipEl(c)) return;
    if (c.classList.contains('etb-concept')) {
      var lb = c.querySelector('.etb-slbl, .etb-kicker'), h = c.querySelector('h2,h3'), lbt = lb ? textOf(lb) : '';
      k++;
      cs = newSec('concept-' + k, h ? squish(h.textContent) : lbt, lbt.replace(/^Major concept/i, 'Concept') || 'Concept ' + k, lb);
      secs[cs].els.push(c);
      walk(c, cs);
      return;
    }
    for (var i = 0; i < MAJOR.length; i++) {
      var m = MAJOR[i];
      if (c.classList.contains(m[0])) {
        var te = m[2] && c.querySelector(m[2]);
        cs = newSec(m[0].replace('etb-', ''), te ? textOf(te) : m[1], m[1], m[3] && c.querySelector(m[3]));
        break;
      }
    }
    if (!c.classList.contains('etb-slbl')) secs[cs].els.push(c);
    handle(c, cs);
  });

  /* Drop sections with nothing to read, then lay out the timeline */
  var keep = secs.map(function (s, i) { return units.some(function (u) { return u.sec === i; }); });
  var remap = [], nsecs = [];
  secs.forEach(function (s, i) { if (keep[i]) { remap[i] = nsecs.length; nsecs.push(s); } });
  units.forEach(function (u) { u.sec = remap[u.sec]; });
  blocks.forEach(function (b) { b.sec = remap[b.sec]; });
  secs = nsecs;
  if (!units.length) return;

  var SEC, total = 0;
  function layout() {
    total = 0;
    SEC.forEach(function (s) { s.start = total; total += s.dur; });
  }
  if (FILES) {
    var base = D.base || '';
    SEC = D.sections.map(function (d) {
      var x = secs.filter(function (s) { return s.id === d.id; })[0] || { els: [], anchor: null };
      return { id: d.id, title: d.title, label: d.label, src: base + d.audio, dur: d.est_seconds || 0, els: x.els, anchor: x.anchor };
    });
  } else {
    SEC = secs;
    var t = 0;
    units.forEach(function (u) { u.start = t; t += u.dur; });
    SEC.forEach(function (s, i) {
      var us = units.filter(function (u) { return u.sec === i; });
      s.first = units.indexOf(us[0]);
      s.dur = us.reduce(function (a, u) { return a + u.dur; }, 0);
    });
  }
  layout();

  var KEY = 'etb-audio:' + (D && D.book || location.pathname) + ':' + (num || chapTitle);
  var HL = !!(window.CSS && CSS.highlights && typeof window.Highlight === 'function');
  var reduceMotion = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ================= Icons ================= */
  var PLAY = '<svg viewBox="0 0 9 10" aria-hidden="true"><path d="M0 0l9 5-9 5z"/></svg>';
  var EQ = '<span class="etb-eq" aria-hidden="true"><i></i><i></i><i></i></span>';
  var ICON = {
    back15: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.4-5.7"/><path d="M4 3v4h4"/></svg><span>15</span>',
    fwd15: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12a8 8 0 1 1-2.4-5.7"/><path d="M20 3v4h-4"/></svg><span>15</span>',
    prev: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17 6l-8 6 8 6z"/><path d="M7 6v12"/></svg>',
    next: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 6l8 6-8 6z"/><path d="M17 6v12"/></svg>',
    list: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6h11M9 12h11M9 18h11"/><path d="M4.5 6h.01M4.5 12h.01M4.5 18h.01"/></svg>',
    close: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    down: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>',
    doc: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/></svg>'
  };

  /* ================= Title card: Listen + Text-only ================= */
  var pill = null, pillText = null;
  if (card) {
    var row = el('div', 'etb-title-listen');
    pill = el('button', 'etb-listen-pill', '<span class="etb-listen-ico">' + PLAY + '</span><span class="etb-listen-txt">Listen</span><span class="etb-listen-len">· ' + mins(total) + '</span>');
    pill.type = 'button';
    pillText = pill.querySelector('.etb-listen-txt');
    row.appendChild(pill);
    var txt = el('button', 'etb-textonly', 'Text-only version');
    txt.type = 'button';
    txt.addEventListener('click', openReader);
    row.appendChild(txt);
    card.insertBefore(row, card.querySelector('.etb-title-meta'));
    pill.addEventListener('click', function () { openPlayer(); E.start(resumeAt()); });
  }

  /* ================= "Listen" on each section header ================= */
  SEC.forEach(function (s, i) {
    var host = s.anchor;
    if (!host) return;
    var b = el('button', 'etb-listen-here', PLAY + EQ + '<span class="etb-listen-word">Listen</span><span class="etb-listen-len">· ' + fmt(s.dur) + '</span>');
    b.type = 'button';
    b.setAttribute('aria-label', 'Listen from ' + s.title);
    b.addEventListener('click', function () {
      if (E.cur() === i && E.playing()) { E.pause(); return; }
      openPlayer(); E.start(s.start);
    });
    host.classList.add('etb-has-listen');
    host.appendChild(b);
    s.btn = b;
  });

  /* ================= The docked player ================= */
  var ap = el('div', 'etb-ap');
  ap.setAttribute('role', 'region');
  ap.setAttribute('aria-label', 'Chapter audio');
  ap.innerHTML =
    '<div class="etb-ap-in">' +
      '<div class="etb-ap-top">' +
        '<button type="button" class="etb-ap-now" title="Show this part of the chapter"><span class="etb-ap-kicker"></span><span class="etb-ap-title"></span></button>' +
        '<div class="etb-ap-tools">' +
          '<button type="button" class="etb-ap-tool etb-ap-speed" aria-label="Playback speed">1×</button>' +
          '<button type="button" class="etb-ap-tool etb-ap-list" aria-label="Contents and settings" aria-expanded="false">' + ICON.list + '</button>' +
          '<button type="button" class="etb-ap-tool etb-ap-close" aria-label="Close player">' + ICON.close + '</button>' +
        '</div>' +
      '</div>' +
      '<div class="etb-ap-bot">' +
        '<button type="button" class="etb-ap-skip etb-ap-back"></button>' +
        '<button type="button" class="etb-ap-play" aria-label="Play"><svg class="i-play" viewBox="0 0 9 10" aria-hidden="true"><path d="M0 0l9 5-9 5z"/></svg><svg class="i-pause" viewBox="0 0 14 16" aria-hidden="true"><rect x="1" y="1" width="4" height="14" rx="1"/><rect x="9" y="1" width="4" height="14" rx="1"/></svg></button>' +
        '<button type="button" class="etb-ap-skip etb-ap-fwd"></button>' +
        '<span class="etb-ap-time etb-ap-cur">0:00</span>' +
        '<div class="etb-ap-track"><div class="etb-ap-rail"><div class="etb-ap-fill"></div></div><div class="etb-ap-thumb"></div><div class="etb-ap-tip"></div><input type="range" min="0" max="1000" step="1" value="0" aria-label="Seek"></div>' +
        '<span class="etb-ap-time etb-ap-dur is-end">0:00</span>' +
      '</div>' +
    '</div>' +
    '<div class="etb-ap-menu" role="dialog" aria-label="Chapter audio contents"></div>';
  document.body.appendChild(ap);

  function q(s) { return ap.querySelector(s); }
  var kicker = q('.etb-ap-kicker'), titleOut = q('.etb-ap-title'), playBtn = q('.etb-ap-play'),
    backBtn = q('.etb-ap-back'), fwdBtn = q('.etb-ap-fwd'),
    curT = q('.etb-ap-cur'), durT = q('.etb-ap-dur'), track = q('.etb-ap-track'), rail = q('.etb-ap-rail'),
    fill = q('.etb-ap-fill'), thumb = q('.etb-ap-thumb'), tip = q('.etb-ap-tip'), range = q('.etb-ap-track input'),
    speedBtn = q('.etb-ap-speed'), listBtn = q('.etb-ap-list'), menu = q('.etb-ap-menu');

  backBtn.innerHTML = TTS ? ICON.prev : ICON.back15;
  fwdBtn.innerHTML = TTS ? ICON.next : ICON.fwd15;
  backBtn.setAttribute('aria-label', TTS ? 'Previous sentence' : 'Back 15 seconds');
  fwdBtn.setAttribute('aria-label', TTS ? 'Next sentence' : 'Forward 15 seconds');
  backBtn.title = backBtn.getAttribute('aria-label');
  fwdBtn.title = fwdBtn.getAttribute('aria-label');

  var RATES = [0.75, 1, 1.25, 1.5, 1.75, 2];
  var rate = store('etb-audio:rate') || 1;
  if (RATES.indexOf(rate) < 0) rate = 1;
  var dragging = false, shown = -1, notice = '';

  /* ================= UI state ================= */
  function sectionAt(t) { for (var i = SEC.length - 1; i >= 0; i--) if (t >= SEC[i].start - 0.01) return i; return 0; }
  function resumeAt() { var v = store(KEY); return v && v.t > 15 && v.t < total - 15 ? v.t : 0; }

  function markCurrent(i) {
    if (i === shown && !notice) return;
    shown = i;
    SEC.forEach(function (s, j) {
      s.els.forEach(function (e) { e.classList.toggle('etb-audio-current', j === i); });
      if (s.btn) s.btn.classList.toggle('is-current', j === i);
    });
    wordState();
    var s = SEC[i];
    if (!s) return;
    kicker.innerHTML = '<span class="etb-ap-ch">' + (num ? 'Chapter ' + esc(num) + ' · ' : '') + '</span>' + esc(s.label) + (D && D.placeholder ? '<span class="etb-ap-demo">· Placeholder audio</span>' : '');
    titleOut.textContent = notice || s.title;
    menu.querySelectorAll('.etb-ap-item').forEach(function (b) { b.classList.toggle('is-current', +b.getAttribute('data-i') === i); });
    if (FILES && 'mediaSession' in navigator && window.MediaMetadata) {
      navigator.mediaSession.metadata = new MediaMetadata({ title: s.title, artist: D.author || '', album: (D.book_title ? D.book_title + ' · ' : '') + (num ? 'Chapter ' + num : chapTitle) });
    }
  }
  function wordState() {
    var on = E && E.playing();
    SEC.forEach(function (s, j) {
      if (s.btn) s.btn.querySelector('.etb-listen-word').textContent = j !== shown ? 'Listen' : (on ? 'Playing' : 'Paused');
    });
  }
  function setPlaying(on) {
    document.documentElement.classList.toggle('etb-playing', on);
    playBtn.setAttribute('aria-label', on ? 'Pause' : 'Play');
    if (!on) save();
    wordState();
    updatePill();
  }
  function paint(t) {
    if (t === undefined) t = E.time();
    var p = total ? Math.min(1, t / total) : 0;
    fill.style.width = (p * 100) + '%';
    thumb.style.left = (p * 100) + '%';
    if (!dragging) range.value = Math.round(p * 1000);
    curT.textContent = fmt(t);
    durT.textContent = fmt(total);
    range.setAttribute('aria-valuetext', fmt(t) + ' of ' + fmt(total));
  }
  function paintTicks() {
    rail.querySelectorAll('.etb-ap-tick').forEach(function (x) { x.remove(); });
    for (var i = 1; i < SEC.length; i++) { var x = el('div', 'etb-ap-tick'); x.style.left = (SEC[i].start / total * 100) + '%'; rail.appendChild(x); }
  }
  function save() { if (E && E.cur() >= 0) store(KEY, { t: E.time() }); }
  function updatePill() {
    if (!pillText) return;
    var r = (E && E.playing()) ? 0 : resumeAt();
    pillText.textContent = r ? 'Resume · ' + fmt(r) : 'Listen';
    pill.querySelector('.etb-listen-len').style.display = r ? 'none' : '';
  }
  function setNotice(msg) { notice = msg; titleOut.textContent = msg || (SEC[shown] ? SEC[shown].title : ''); }

  function buildMenu() {
    var h = '<div class="etb-ap-menu-h">In this chapter</div>';
    SEC.forEach(function (s, i) {
      h += '<button type="button" class="etb-ap-item' + (i === shown ? ' is-current' : '') + '" data-i="' + i + '"><span class="etb-ap-item-n">' + (i + 1) + '</span><span class="etb-ap-item-t"><small>' + esc(s.label) + '</small>' + esc(s.title) + '</span><span class="etb-ap-item-d">' + fmt(s.dur) + '</span></button>';
    });
    h += '<div class="etb-ap-menu-foot">';
    if (TTS) h += '<div class="etb-ap-voice"><label for="etb-ap-voice-select">Voice</label><select id="etb-ap-voice-select"></select><p>Read aloud by your device. Different browsers offer different voices.</p></div>';
    if (FILES && D.full_url) h += '<a href="' + esc(D.full_url) + '" download>' + ICON.down + 'Download the whole chapter (MP3) <span>' + mins(total) + '</span></a>';
    h += '<button type="button" class="etb-ap-link etb-ap-text">' + ICON.doc + 'Text-only version</button>';
    h += '</div>';
    menu.innerHTML = h;
    menu.querySelectorAll('.etb-ap-item').forEach(function (b) {
      b.addEventListener('click', function () { E.start(SEC[+b.getAttribute('data-i')].start); toggleMenu(false); });
    });
    menu.querySelector('.etb-ap-text').addEventListener('click', function () { toggleMenu(false); openReader(); });
    if (TTS) { fillVoices(); menu.querySelector('select').addEventListener('change', function (e) { pickVoice(e.target.value); }); }
  }
  function toggleMenu(force) {
    var on = force !== undefined ? force : !menu.classList.contains('is-open');
    menu.classList.toggle('is-open', on);
    listBtn.setAttribute('aria-expanded', on ? 'true' : 'false');
  }

  /* ================= Device voice ================= */
  var voices = [], voice = null, VKEY = 'etb-audio:voice';
  function rank(v) {
    var n = v.name, s = 0;
    if (/natural|neural/i.test(n)) s += 50;
    if (/premium|enhanced/i.test(n)) s += 40;
    if (/siri/i.test(n)) s += 30;
    if (/google/i.test(n)) s += 20;
    if (/en[-_]US/i.test(v.lang)) s += 6;
    if (/en[-_](GB|AU|CA|IE|NZ)/i.test(v.lang)) s += 3;
    if (v.localService) s += 1;
    if (/albert|bad news|bahh|bells|boing|bubbles|cellos|deranged|good news|hysterical|jester|junior|organ|superstar|trinoids|whisper|wobble|zarvox|ralph|fred|kathy|grandma|grandpa|rocko|shelley|eloquence|compact/i.test(n)) s -= 80;
    return s;
  }
  function loadVoices() {
    if (!TTS) return;
    voices = synth.getVoices().filter(function (v) { return /^en([-_]|$)/i.test(v.lang); }).sort(function (a, b) { return rank(b) - rank(a); });
    var want = store(VKEY);
    voice = voices.filter(function (v) { return v.name === want; })[0] || voices[0] || null;
    fillVoices();
  }
  function fillVoices() {
    var sel = menu.querySelector('#etb-ap-voice-select');
    if (!sel) return;
    sel.innerHTML = voices.length ? voices.slice(0, 40).map(function (v) {
      return '<option value="' + esc(v.name) + '"' + (voice && v.name === voice.name ? ' selected' : '') + '>' + esc(v.name.replace(/^Microsoft\s+/, '').replace(/\s+-\s+English.*$/, '')) + ' (' + esc(v.lang) + ')</option>';
    }).join('') : '<option>Your browser’s default voice</option>';
  }
  function pickVoice(name) {
    voice = voices.filter(function (v) { return v.name === name; })[0] || voice;
    store(VKEY, voice ? voice.name : null);
    if (E.playing()) E.restart();
  }

  var highlighted = null;
  function clearHighlight() {
    if (HL) CSS.highlights.delete('etb-reading');
    if (highlighted) { highlighted.classList.remove('etb-reading-el'); highlighted = null; }
  }
  function showUnit(u) {
    clearHighlight();
    if (u.range && HL) CSS.highlights.set('etb-reading', new Highlight(u.range));
    else if (u.el) { u.el.classList.add('etb-reading-el'); highlighted = u.el; }
    markCurrent(u.sec);
    follow(u);
  }
  /* Keep the sentence on screen unless the reader has scrolled away on purpose */
  var userScrolled = 0;
  ['wheel', 'touchmove'].forEach(function (ev) { window.addEventListener(ev, function () { userScrolled = Date.now(); }, { passive: true }); });
  window.addEventListener('keydown', function (e) { if (/^(Arrow(Up|Down)|Page(Up|Down)|Home|End| )$/.test(e.key) && !ap.contains(e.target)) userScrolled = Date.now(); });
  function follow(u) {
    if (Date.now() - userScrolled < 6000 || reader.open) return;
    var target = u.range || u.el;
    if (!target) return;
    var r = target.getBoundingClientRect(), bottom = window.innerHeight - ap.offsetHeight - 24;
    if (r.top < 48 || r.bottom > bottom) window.scrollBy({ top: r.top - window.innerHeight * 0.3, behavior: reduceMotion ? 'auto' : 'smooth' });
  }

  function ttsEngine() {
    var idx = -1, gen = 0, on = false, t0 = 0, keepAlive = null, errors = 0;
    function cancel() { gen++; clearInterval(keepAlive); if (synth.speaking || synth.pending) synth.cancel(); }
    function finish() { on = false; idx = -1; clearHighlight(); store(KEY, { t: 0 }); setPlaying(false); paint(total); }
    function go(i, g) {
      if (g !== gen) return;
      if (i >= units.length) { finish(); return; }
      idx = i; t0 = now();
      var u = units[i], p = 0;
      showUnit(u);
      (function next() {
        if (g !== gen) return;
        if (p >= u.parts.length) {
          if (u.gap) setTimeout(function () { go(i + 1, g); }, u.gap * 1000 / rate); else go(i + 1, g);
          return;
        }
        var ut = new SpeechSynthesisUtterance(u.parts[p++]);
        ut.rate = rate;
        ut.lang = voice ? voice.lang : 'en-US';
        if (voice) ut.voice = voice;
        ut.onend = function () { errors = 0; next(); };
        ut.onerror = function (e) {
          if (g !== gen || e.error === 'interrupted' || e.error === 'canceled') return;
          if (++errors >= 3 || e.error === 'not-allowed') {
            cancel(); on = false; setPlaying(false);
            setNotice('Your browser couldn’t start its reading voice. Try another browser, or use the text-only version.');
            return;
          }
          next();
        };
        synth.speak(ut);
      })();
    }
    function speakFrom(i) {
      var busy = synth.speaking || synth.pending;
      cancel();
      var g = gen;
      on = true; idx = i; t0 = now(); errors = 0;
      setNotice('');
      setPlaying(true);
      showUnit(units[i]);
      if (busy) setTimeout(function () { go(i, g); }, 80); else go(i, g);
      if (voice && !voice.localService) keepAlive = setInterval(function () { if (synth.speaking && !synth.paused) { synth.pause(); synth.resume(); } }, 10000);
    }
    function unitAt(t) { for (var i = units.length - 1; i >= 0; i--) if (t >= units[i].start - 0.01) return i; return 0; }
    function park(i) { idx = i; t0 = now(); showUnit(units[i]); paint(); }
    window.addEventListener('pagehide', function () { cancel(); });
    return {
      start: function (t) { speakFrom(unitAt(t || 0)); },
      playing: function () { return on; },
      cur: function () { return idx < 0 ? -1 : units[idx].sec; },
      time: function () { return idx < 0 ? 0 : units[idx].start + (on ? Math.min(units[idx].dur, (now() - t0) / 1000 * rate) : 0); },
      toggle: function () { if (on) this.pause(); else speakFrom(idx < 0 ? unitAt(resumeAt()) : idx); },
      pause: function () { cancel(); on = false; setPlaying(false); },
      restart: function () { if (idx >= 0) speakFrom(idx); },
      back: function () {
        if (idx < 0) return;
        var into = (now() - t0) / 1000 * rate, i = (on && into > 2) ? idx : Math.max(0, idx - 1);
        if (on) speakFrom(i); else park(i);
      },
      fwd: function () { if (idx < 0) return; var i = Math.min(units.length - 1, idx + 1); if (on) speakFrom(i); else park(i); },
      seek: function (t) { var i = unitAt(t); if (on) speakFrom(i); else park(i); },
      setRate: function () { if (on) speakFrom(idx); },
      stop: function () { cancel(); on = false; idx = -1; clearHighlight(); }
    };
  }

  /* ================= Recorded audio (MP3s) ================= */
  function fileEngine() {
    var audio = new Audio(), cur = -1;
    audio.preload = 'metadata';
    /* Real lengths replace the estimates as each file's header loads */
    SEC.forEach(function (s) {
      var a = new Audio();
      a.preload = 'metadata';
      a.addEventListener('loadedmetadata', function () { if (isFinite(a.duration) && a.duration > 0) { s.dur = a.duration; layout(); paintTicks(); buildMenu(); paint(); } });
      a.src = s.src;
    });
    function load(i, local, play) {
      cur = i;
      var go = function () {
        audio.removeEventListener('loadedmetadata', go);
        try { audio.currentTime = local; } catch (e) {}
        audio.defaultPlaybackRate = audio.playbackRate = rate;
        if (play) audio.play().catch(function () {});
      };
      audio.addEventListener('loadedmetadata', go);
      audio.src = SEC[i].src;
      markCurrent(i);
    }
    function seek(t, play) {
      t = Math.max(0, Math.min(total - 0.25, t));
      var i = sectionAt(t), local = t - SEC[i].start;
      if (i !== cur) load(i, local, play !== undefined ? play : !audio.paused);
      else { audio.currentTime = local; if (play) audio.play().catch(function () {}); }
      paint(t);
    }
    var api = {
      start: function (t) { seek(t || 0, true); },
      playing: function () { return cur >= 0 && !audio.paused; },
      cur: function () { return cur; },
      time: function () { return cur < 0 ? 0 : SEC[cur].start + (audio.currentTime || 0); },
      toggle: function () { if (cur < 0) { seek(resumeAt(), true); return; } if (audio.paused) audio.play().catch(function () {}); else audio.pause(); },
      pause: function () { audio.pause(); },
      restart: function () {},
      back: function () { seek(api.time() - 15); },
      fwd: function () { seek(api.time() + 15); },
      seek: function (t) { seek(t); },
      setRate: function () { audio.defaultPlaybackRate = audio.playbackRate = rate; },
      stop: function () { audio.pause(); cur = -1; audio.removeAttribute('src'); audio.load(); }
    };
    audio.addEventListener('play', function () { setPlaying(true); });
    audio.addEventListener('pause', function () { setPlaying(false); });
    audio.addEventListener('ended', function () { if (cur < SEC.length - 1) load(cur + 1, 0, true); else { store(KEY, { t: 0 }); setPlaying(false); } });
    if ('mediaSession' in navigator) {
      var ms = navigator.mediaSession;
      try {
        ms.setActionHandler('play', function () { audio.play(); });
        ms.setActionHandler('pause', function () { audio.pause(); });
        ms.setActionHandler('seekbackward', api.back);
        ms.setActionHandler('seekforward', api.fwd);
        ms.setActionHandler('previoustrack', function () { seek(SEC[Math.max(0, cur - 1)].start); });
        ms.setActionHandler('nexttrack', function () { if (cur < SEC.length - 1) seek(SEC[cur + 1].start); });
      } catch (e) {}
    }
    return api;
  }

  var E = TTS ? ttsEngine() : fileEngine();

  /* ================= Controls ================= */
  playBtn.addEventListener('click', function () { E.toggle(); });
  backBtn.addEventListener('click', function () { E.back(); paint(); });
  fwdBtn.addEventListener('click', function () { E.fwd(); paint(); });
  speedBtn.textContent = rate + '×';
  speedBtn.addEventListener('click', function () {
    rate = RATES[(RATES.indexOf(rate) + 1) % RATES.length];
    speedBtn.textContent = rate + '×';
    store('etb-audio:rate', rate);
    E.setRate();
  });
  listBtn.addEventListener('click', function (e) { e.stopPropagation(); toggleMenu(); });
  menu.addEventListener('click', function (e) { e.stopPropagation(); });
  document.addEventListener('click', function () { toggleMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { if (reader.open) closeReader(); else toggleMenu(false); } });
  q('.etb-ap-now').addEventListener('click', function () {
    var s = SEC[E.cur() < 0 ? shown : E.cur()], e = s && s.els[0];
    userScrolled = 0;
    if (e) e.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
  });
  range.addEventListener('input', function () { dragging = true; track.classList.add('is-drag'); paint(range.value / 1000 * total); });
  range.addEventListener('change', function () { dragging = false; track.classList.remove('is-drag'); userScrolled = 0; E.seek(range.value / 1000 * total); paint(); });
  track.addEventListener('mousemove', function (e) {
    var r = track.getBoundingClientRect(), p = Math.min(1, Math.max(0, (e.clientX - r.left) / r.width)), t = p * total;
    tip.innerHTML = '<b>' + fmt(t) + '</b>' + esc(SEC[sectionAt(t)].title);
    tip.style.left = Math.min(r.width - 60, Math.max(60, p * r.width)) + 'px';
  });
  function openPlayer() { ap.classList.add('is-open'); root.classList.add('etb-audio-on'); userScrolled = 0; }
  q('.etb-ap-close').addEventListener('click', function () {
    save();
    E.stop();
    ap.classList.remove('is-open');
    root.classList.remove('etb-audio-on');
    SEC.forEach(function (s) { s.els.forEach(function (e) { e.classList.remove('etb-audio-current'); }); if (s.btn) s.btn.classList.remove('is-current'); });
    shown = -1;
    toggleMenu(false);
    setPlaying(false);
    if (pill) pill.focus();
  });
  var lastSave = 0;
  setInterval(function () {
    if (!E.playing() || dragging) return;
    paint();
    if (Date.now() - lastSave > 4000) { lastSave = Date.now(); save(); }
  }, 250);

  /* ================= Text-only reading view ================= */
  var reader = { open: false, node: null, back: null };
  function buildReader() {
    var h = '<div class="etb-rv-bar"><div class="etb-rv-bar-in"><span>Text-only version</span><button type="button" class="etb-rv-close">Back to the chapter</button></div></div><article class="etb-rv-in">';
    h += '<h1>' + esc(num ? 'Chapter ' + num + ': ' + chapTitle : chapTitle) + '</h1>';
    if (subEl) h += '<p class="etb-rv-sub">' + esc(squish(subEl.textContent)) + '</p>';
    var lastSec = 0;
    blocks.forEach(function (b) {
      var s = secs[b.sec];
      if (b.sec !== lastSec && s) { lastSec = b.sec; h += '<h2><small>' + esc(s.label) + '</small>' + esc(s.title) + '</h2>'; }
      if (!b.text || /^(chapter|title|subtitle)$/.test(b.kind)) return;
      if (b.kind === 'label' && s && b.el === s.anchor) return;
      if (b.kind === 'heading') { if (!s || b.text !== s.title) h += '<h3>' + esc(b.text) + '</h3>'; return; }
      if (b.kind === 'label' || b.kind === 'minor') { h += '<p class="etb-rv-minor">' + esc(b.text) + '</p>'; return; }
      if (b.kind === 'prompt') { h += '<p class="etb-rv-prompt">' + esc(b.text) + '</p>'; return; }
      h += '<p>' + esc(b.text) + '</p>';
    });
    h += '</article>';
    var n = el('div', 'etb-rv', h);
    n.setAttribute('role', 'dialog');
    n.setAttribute('aria-modal', 'true');
    n.setAttribute('aria-label', 'Text-only version of ' + chapTitle);
    n.tabIndex = -1;
    n.hidden = true;
    n.querySelector('.etb-rv-close').addEventListener('click', closeReader);
    document.body.appendChild(n);
    return n;
  }
  function openReader() {
    if (!reader.node) reader.node = buildReader();
    reader.back = document.activeElement;
    reader.node.hidden = false;
    reader.open = true;
    document.documentElement.style.overflow = 'hidden';
    reader.node.scrollTop = 0;
    reader.node.querySelector('.etb-rv-close').focus();
  }
  function closeReader() {
    if (!reader.node) return;
    reader.node.hidden = true;
    reader.open = false;
    document.documentElement.style.overflow = '';
    if (reader.back && reader.back.focus) reader.back.focus();
  }

  /* ================= Start ================= */
  buildMenu();
  if (TTS) { loadVoices(); if (synth.addEventListener) synth.addEventListener('voiceschanged', loadVoices); else synth.onvoiceschanged = loadVoices; }
  paintTicks();
  paint(0);
  updatePill();
})();
