/*
 * report.js: the "Report a problem" button for the textbook sites.
 *
 * Shared by both books. The source lives in feedback/report.js in each textbook
 * repository, and the two copies must stay identical. The builds copy it into the
 * published folder; never edit that copy.
 *
 * Adds a "Report a problem" card at the end of the chapter and a small Report button
 * in the floating chapter bar. Reports go to /api/report on the same site, where
 * feedback/worker.js files them as issues in the private textbook-feedback repo.
 *
 * Load it on chapter pages with the book's name:
 *   <script src="/assets/report.js" data-book="EDCOR 310" defer></script>
 */
(function () {
  'use strict';
  if (window.__etbReport) return;
  window.__etbReport = true;

  var script = document.currentScript;
  var BOOK = (script && script.getAttribute('data-book')) || document.title.split('·').pop().trim();
  var ENDPOINT = '/api/report';

  var CSS = [
    '.efb{--efb-ink:#1a1a1a;--efb-muted:#5f6670;--efb-navy:#1a3a5c;--efb-navy-hover:#244d78;--efb-green:#2a7a4f;--efb-line:#dde2e8;--efb-field:#c6ccd5;--efb-paper:#fff;--efb-soft:#f4f6f9;--efb-chip:#eef3f8;--efb-err:#a33030;--efb-ring:#8fb3d9;--efb-sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;--efb-serif:Georgia,"Times New Roman",serif;font-family:var(--efb-serif);color:var(--efb-ink);box-sizing:border-box}',
    '.efb *,.efb *::before,.efb *::after{box-sizing:border-box}',
    '.efb-end{max-width:740px;margin:2.5rem auto 2.5rem;padding:0 1rem}',
    '.efb-card{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1rem;border:1px solid var(--efb-line);border-radius:10px;background:var(--efb-soft);padding:1.1rem 1.25rem}',
    '.efb-card p{margin:0;font-size:15.5px;line-height:1.55;color:var(--efb-muted);flex:1 1 18rem;min-width:0}',
    '.efb-card strong{color:var(--efb-ink);font-weight:700}',
    '.efb-btn{font-family:var(--efb-sans);font-size:14px;font-weight:600;line-height:1.2;border-radius:8px;padding:.65rem 1.05rem;cursor:pointer;border:1px solid var(--efb-navy);background:var(--efb-navy);color:var(--efb-paper)}',
    '.efb-btn:hover{background:var(--efb-navy-hover);border-color:var(--efb-navy-hover)}',
    '.efb-btn[disabled]{opacity:.6;cursor:default}',
    '.efb-btn-quiet{background:transparent;color:var(--efb-navy)}',
    '.efb-btn-quiet:hover{background:var(--efb-chip);color:var(--efb-navy)}',
    '.efb-btn:focus-visible,.efb-type input:focus-visible+span,.efb select:focus-visible,.efb textarea:focus-visible,.efb input[type=text]:focus-visible,.efb-x:focus-visible,.etb-nav .etb-nav-report:focus-visible{outline:3px solid var(--efb-ring,#8fb3d9);outline-offset:2px}',
    '.efb-overlay{display:none;position:fixed;inset:0;z-index:10000;background:rgba(18,26,36,.55);align-items:flex-start;justify-content:center;padding:5vh 1rem 2rem;overflow-y:auto}',
    '.efb-overlay.efb-open{display:flex}',
    '.efb-dialog{position:relative;background:var(--efb-paper);color:var(--efb-ink);border-radius:12px;width:100%;max-width:520px;padding:1.5rem 1.5rem 1.25rem;box-shadow:0 12px 40px rgba(0,0,0,.28);font-family:var(--efb-sans)}',
    '.efb-dialog h3{font-family:var(--efb-serif);font-size:21px;line-height:1.25;margin:0 2rem .3rem 0;color:var(--efb-ink)}',
    '.efb-sub{font-size:13.5px;line-height:1.5;color:var(--efb-muted);margin:0 0 1.15rem}',
    '.efb-x{position:absolute;top:.75rem;right:.75rem;width:2.1rem;height:2.1rem;border:0;border-radius:6px;background:transparent;color:var(--efb-muted);font-size:22px;line-height:1;cursor:pointer}',
    '.efb-x:hover{background:var(--efb-soft);color:var(--efb-ink)}',
    '.efb-field{display:flex;flex-direction:column;gap:.4rem;margin:0 0 1rem;border:0;padding:0;min-width:0}',
    '.efb-label{font-size:13px;font-weight:600;color:var(--efb-ink);padding:0}',
    '.efb-hint{font-weight:400;color:var(--efb-muted)}',
    '.efb select,.efb textarea,.efb input[type=text]{font-family:var(--efb-sans);font-size:15px;line-height:1.4;padding:.55rem .65rem;border:1px solid var(--efb-field);border-radius:8px;background:var(--efb-paper);color:var(--efb-ink);width:100%;max-width:100%}',
    '.efb textarea{min-height:110px;resize:vertical}',
    '.efb-types{display:grid;grid-template-columns:1fr 1fr;gap:.45rem}',
    '.efb-type{position:relative;display:block;cursor:pointer}',
    '.efb-type input{position:absolute;opacity:0;width:1px;height:1px}',
    '.efb-type span{display:block;height:100%;font-size:13.5px;line-height:1.35;padding:.55rem .65rem;border:1px solid var(--efb-field);border-radius:8px;background:var(--efb-paper);color:var(--efb-ink)}',
    '.efb-type span small{display:block;font-size:12px;color:var(--efb-muted);margin-top:.1rem}',
    '.efb-type input:checked+span{border-color:var(--efb-navy);background:var(--efb-chip);box-shadow:inset 0 0 0 1px var(--efb-navy)}',
    '.efb-quote{display:none;font-size:13.5px;line-height:1.5;background:var(--efb-soft);border-left:3px solid var(--efb-green);border-radius:0 6px 6px 0;padding:.55rem .7rem;margin:0 0 1rem;color:var(--efb-muted);font-family:var(--efb-serif);font-style:italic}',
    '.efb-quote.efb-show{display:block}',
    '.efb-quote button{font-family:var(--efb-sans);font-style:normal;font-size:12px;border:0;background:none;color:var(--efb-navy);text-decoration:underline;cursor:pointer;padding:0;margin-left:.35rem}',
    '.efb-auto{font-size:12px;line-height:1.5;color:var(--efb-muted);margin:0 0 1rem}',
    '.efb-error{display:none;font-size:13px;color:var(--efb-err);margin:-.5rem 0 1rem}',
    '.efb-error.efb-show{display:block}',
    '.efb-actions{display:flex;gap:.6rem;justify-content:flex-end;flex-wrap:wrap}',
    '.efb-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}',
    '.efb-done{display:none}',
    '.efb-done.efb-show{display:block}',
    '.efb-done p{font-size:14.5px;line-height:1.55;color:var(--efb-ink);margin:0 0 1rem}',
    '.etb-nav .etb-nav-report{display:inline-flex;align-items:center;justify-content:center;gap:5px;min-height:34px;padding:0 11px;border:1px solid #d6e0e8;border-radius:6px;color:#1a3a5c;background:#fff;font:700 12px Arial,sans-serif;white-space:nowrap;cursor:pointer}',
    '.etb-nav .etb-nav-report:hover{background:#eef4fb;border-color:#9aaebe}',
    '.etb-nav .etb-nav-report svg{width:12px;height:12px}',
    '@media (max-width:620px){.etb-nav .etb-nav-report{min-height:32px;padding:0 8px;font-size:11px}}',
    '@media (max-width:480px){.efb-types{grid-template-columns:1fr}.efb-dialog{padding:1.25rem 1.1rem 1.1rem}}',
    '@media (prefers-reduced-motion:no-preference){.efb-dialog{animation:efb-in .16s ease-out}@keyframes efb-in{from{transform:translateY(8px)}to{transform:none}}}'
  ].join('\n');

  var TYPES = [
    ['Typo or wording', ''],
    ['Something is broken', 'graph, widget, homework, link'],
    ['Looks wrong on my screen', 'spacing, layout, cut off'],
    ['Content is unclear or seems wrong', ''],
    ['Something else', '']
  ];

  var FLAG = '<svg viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M3 1.5a.75.75 0 0 1 .75.75V3h8.06a.75.75 0 0 1 .6 1.2L10.94 6.25l1.47 2.05a.75.75 0 0 1-.6 1.2H3.75v5.25a.75.75 0 0 1-1.5 0V2.25A.75.75 0 0 1 3 1.5Z"/></svg>';

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }
  function text(el) { return (el && el.textContent || '').replace(/\s+/g, ' ').trim(); }

  function build() {
    var style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    var types = TYPES.map(function (t, i) {
      return '<label class="efb-type"><input type="radio" name="efb-type" value="' + esc(t[0]) + '"' + (i === 0 ? ' checked' : '') + '><span>' +
        esc(t[0]) + (t[1] ? '<small>' + esc(t[1]) + '</small>' : '') + '</span></label>';
    }).join('');

    var end = document.createElement('div');
    end.className = 'efb efb-end';
    end.id = 'efb-root';
    end.innerHTML =
      '<div class="efb-card"><p><strong>Spot a problem in this chapter?</strong> Typos, a graph that won’t work, spacing that looks off on your phone. Tell us and we’ll fix it.</p>' +
      '<button type="button" class="efb-btn" data-efb-open>Report a problem</button></div>';

    var overlay = document.createElement('div');
    overlay.className = 'efb efb-overlay';
    overlay.innerHTML =
      '<div class="efb-dialog" role="dialog" aria-modal="true" aria-labelledby="efb-title">' +
        '<button type="button" class="efb-x" data-efb-close aria-label="Close">&times;</button>' +
        '<div data-efb-form>' +
          '<h3 id="efb-title">Report a problem</h3>' +
          '<p class="efb-sub">This goes straight to the authors. A sentence or two is plenty.</p>' +
          '<fieldset class="efb-field"><legend class="efb-label">What kind of problem?</legend><div class="efb-types">' + types + '</div></fieldset>' +
          '<div class="efb-field"><label class="efb-label" for="efb-section">Where in the chapter?</label><select id="efb-section"></select></div>' +
          '<div class="efb-quote" data-efb-quote></div>' +
          '<div class="efb-field"><label class="efb-label" for="efb-details">What’s wrong?</label>' +
            '<textarea id="efb-details" maxlength="4000" placeholder="Example: The graph in the second section won’t let me drag the line on my phone."></textarea></div>' +
          '<p class="efb-error" data-efb-error></p>' +
          '<div class="efb-field"><label class="efb-label" for="efb-contact">Your name or email <span class="efb-hint">(optional, only if you’d like a reply)</span></label>' +
            '<input type="text" id="efb-contact" maxlength="200" autocomplete="email"></div>' +
          '<div class="efb-hp" aria-hidden="true"><label for="efb-website">Website</label><input type="text" id="efb-website" tabindex="-1" autocomplete="off"></div>' +
          '<p class="efb-auto">We’ll also include the chapter name, this page’s address, and what device and browser you’re using, so we can see the problem the way you do.</p>' +
          '<div class="efb-actions"><button type="button" class="efb-btn efb-btn-quiet" data-efb-close>Cancel</button><button type="button" class="efb-btn" data-efb-send>Send report</button></div>' +
        '</div>' +
        '<div class="efb-done" data-efb-done>' +
          '<h3>Thanks, it’s sent.</h3>' +
          '<p>We’ll take a look. If you left your name or email, you may hear back.</p>' +
          '<div class="efb-actions"><button type="button" class="efb-btn" data-efb-finish>Close</button></div>' +
        '</div>' +
      '</div>';

    var chapter = document.querySelector('.etb');
    if (chapter && chapter.parentNode) chapter.parentNode.insertBefore(end, chapter.nextSibling);
    else (document.querySelector('main') || document.body).appendChild(end);
    document.body.appendChild(overlay);
    return { end: end, overlay: overlay };
  }

  function start() {
    var ui = build();
    var overlay = ui.overlay;
    function q(sel) { return overlay.querySelector(sel); }
    var sectionSel = q('#efb-section'), details = q('#efb-details'), contact = q('#efb-contact');
    var quoteBox = q('[data-efb-quote]'), errorBox = q('[data-efb-error]'), sendBtn = q('[data-efb-send]');
    var lastSelection = '', lastNode = null, lastFocus = null;

    function chapterTitle() {
      // The page title carries the chapter number ("Chapter 22: Attention, ... · The Science of Learning").
      var fromTitle = document.title.split('\u00b7')[0].trim();
      if (/^Chapter\s+\d+/i.test(fromTitle)) return fromTitle;
      return text(document.querySelector('.etb-title-main') || document.querySelector('h1')) || fromTitle;
    }
    function headings() {
      var out = [], all = document.querySelectorAll('.etb h2');
      for (var i = 0; i < all.length && out.length < 40; i++) {
        if (!all[i].classList.contains('etb-title-main') && text(all[i])) out.push(all[i]);
      }
      return out;
    }
    function sectionFor(node, heads) {
      var found = '';
      for (var i = 0; i < heads.length; i++) {
        var pos = heads[i].compareDocumentPosition(node);
        if (pos & Node.DOCUMENT_POSITION_FOLLOWING || pos & Node.DOCUMENT_POSITION_CONTAINED_BY) found = text(heads[i]);
      }
      return found;
    }
    function fillSections(pre) {
      sectionSel.innerHTML = '';
      var opts = ['Not sure / whole chapter'].concat(headings().map(text));
      opts.forEach(function (label) {
        var o = document.createElement('option');
        o.value = o.textContent = label;
        if (pre && label === pre) o.selected = true;
        sectionSel.appendChild(o);
      });
    }
    function device() {
      var ua = navigator.userAgent || '';
      var os = /iPhone/.test(ua) ? 'iPhone' : /iPad/.test(ua) ? 'iPad' : /Android/.test(ua) ? 'Android' :
               /CrOS/.test(ua) ? 'Chromebook' : /Mac OS X/.test(ua) ? 'Mac' : /Windows/.test(ua) ? 'Windows' : /Linux/.test(ua) ? 'Linux' : 'Unknown OS';
      var br = /Edg\//.test(ua) ? 'Edge' : /OPR\//.test(ua) ? 'Opera' : /Firefox\//.test(ua) ? 'Firefox' :
               /CriOS|Chrome\//.test(ua) ? 'Chrome' : /Safari\//.test(ua) ? 'Safari' : 'Unknown browser';
      return os + ', ' + br + ', window ' + window.innerWidth + '×' + window.innerHeight + ' | ' + ua;
    }
    function capture() {
      try {
        var sel = window.getSelection();
        var s = sel ? sel.toString().replace(/\s+/g, ' ').trim() : '';
        if (s && !overlay.contains(sel.anchorNode)) { lastSelection = s.slice(0, 600); lastNode = sel.getRangeAt(0).startContainer; }
      } catch (e) {}
    }
    function showQuote() {
      if (!lastSelection) { quoteBox.classList.remove('efb-show'); quoteBox.textContent = ''; return; }
      var shown = lastSelection.length > 240 ? lastSelection.slice(0, 240).replace(/\s+\S*$/, '') + '…' : lastSelection;
      quoteBox.textContent = 'You highlighted: “' + shown + '”';
      var rm = document.createElement('button');
      rm.type = 'button';
      rm.textContent = 'remove';
      rm.addEventListener('click', function () { lastSelection = ''; lastNode = null; showQuote(); });
      quoteBox.appendChild(rm);
      quoteBox.classList.add('efb-show');
    }
    function setError(msg) {
      errorBox.textContent = msg || '';
      errorBox.classList.toggle('efb-show', !!msg);
    }
    function open() {
      lastFocus = document.activeElement;
      fillSections(lastNode ? sectionFor(lastNode, headings()) : '');
      showQuote();
      setError('');
      q('[data-efb-form]').style.display = '';
      q('[data-efb-done]').classList.remove('efb-show');
      overlay.classList.add('efb-open');
      document.documentElement.style.overflow = 'hidden';
      var checked = q('input[name="efb-type"]:checked');
      if (checked) checked.focus();
    }
    function close() {
      overlay.classList.remove('efb-open');
      document.documentElement.style.overflow = '';
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    function reset() {
      details.value = '';
      contact.value = '';
      lastSelection = '';
      lastNode = null;
      sendBtn.disabled = false;
      sendBtn.textContent = 'Send report';
      close();
    }
    function done() {
      q('[data-efb-form]').style.display = 'none';
      q('[data-efb-done]').classList.add('efb-show');
      q('[data-efb-finish]').focus();
    }
    function send() {
      var typeEl = q('input[name="efb-type"]:checked');
      var report = {
        book: BOOK,
        chapter: chapterTitle(),
        section: sectionSel.value,
        type: typeEl ? typeEl.value : '',
        details: details.value.trim(),
        quote: lastSelection,
        contact: contact.value.trim(),
        page: location.href,
        device: device(),
        website: q('#efb-website').value
      };
      if (!report.details) { setError('Please describe the problem before sending.'); details.focus(); return; }
      setError('');
      sendBtn.disabled = true;
      sendBtn.textContent = 'Sending…';
      fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(report) })
        .then(function (r) { if (!r.ok) throw new Error('status ' + r.status); done(); })
        .catch(function () {
          sendBtn.disabled = false;
          sendBtn.textContent = 'Send report';
          setError('That didn’t send. Check your connection and try again. If it keeps failing, tell your instructor.');
        });
    }
    function wireOpener(btn) {
      btn.addEventListener('pointerdown', capture);
      btn.addEventListener('keydown', capture);
      btn.addEventListener('click', open);
    }

    wireOpener(ui.end.querySelector('[data-efb-open]'));
    overlay.querySelectorAll('[data-efb-close]').forEach(function (b) { b.addEventListener('click', close); });
    q('[data-efb-finish]').addEventListener('click', reset);
    sendBtn.addEventListener('click', send);
    overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });
    overlay.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { close(); return; }
      if (e.key !== 'Tab') return;
      var f = [].filter.call(overlay.querySelectorAll('button:not([disabled]),input:not([tabindex="-1"]),select,textarea'), function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { f[f.length - 1].focus(); e.preventDefault(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { f[0].focus(); e.preventDefault(); }
    });

    // A Report button in the floating chapter bar, so students can report from anywhere in the chapter.
    // The bar may be drawn by another script, so wait briefly for it.
    var tries = 0;
    (function addToBar() {
      var inner = document.querySelector('.etb-nav-inner');
      if (!inner) { if (tries++ < 40) setTimeout(addToBar, 100); return; }
      if (inner.querySelector('.etb-nav-report')) return;
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'etb-nav-report';
      b.setAttribute('aria-label', 'Report a problem with this page');
      b.innerHTML = FLAG + 'Report';  // plain text: the bar styles every <span> as a button
      wireOpener(b);
      var next = inner.lastElementChild;
      inner.insertBefore(b, next);
    })();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
