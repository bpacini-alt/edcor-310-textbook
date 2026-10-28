/* Joy reading menus (Joy of Learning, Joy of Econ): shared behavior.
   Identical copies live in both textbook repositories (menus/joy-menu.js).
   Change both in matching pull requests. The builder inlines this file into each page.

   What it does: lets a student mark readings "I'll read this" or "My group has it",
   see minutes chosen against the requirement, filter the menu, and copy their list.
   Students submit their notes separately, so the page deliberately has no notes box. Everything is saved in this browser only (localStorage).
   The page works without this script; it just has no buttons. */
(function () {
  "use strict";
  var cfgEl = document.getElementById("jm-config");
  if (!cfgEl) return;
  var cfg = JSON.parse(cfgEl.textContent);
  var KEY = cfg.storageKey;
  var revealButton = document.getElementById("jm-reveal-all");
  var allVotesVisible = false;
  var summaries = {};
  var summariesError = false;
  var summariesPromise = null;
  function targetOf(scopeId) { var s = scopeById[scopeId]; return s ? Number(s.dataset.target) || 60 : 60; }

  // ---------- saved state ----------
  var state = { mine: {}, group: {} };
  try {
    var raw = window.localStorage.getItem(KEY);
    if (raw) {
      var parsed = JSON.parse(raw);
      state.mine = parsed.mine || {};
      state.group = parsed.group || {};
    }
  } catch (e) { /* storage blocked or empty: start fresh */ }
  // Returning students already know how it works: start with the instructions folded.
  if (Object.keys(state.mine).length || Object.keys(state.group).length) {
    var howto = document.querySelector(".jm-howto");
    if (howto) howto.open = false;
  }
  var saveTimer = null;
  function save() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () {
      try { window.localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* not saved; page still works */ }
    }, 150);
  }

  var entries = Array.prototype.slice.call(document.querySelectorAll(".jm-entry"));
  var byId = {};
  entries.forEach(function (el) { byId[el.dataset.id] = el; });
  // Drop saved ids that no longer exist in the menu.
  ["mine", "group"].forEach(function (k) {
    Object.keys(state[k]).forEach(function (id) { if (!byId[id]) delete state[k][id]; });
  });

  var scopes = Array.prototype.slice.call(document.querySelectorAll("[data-scope]"));
  var scopeById = {};
  scopes.forEach(function (s) { scopeById[s.dataset.scope] = s; });

  // ---------- toast ----------
  var toast = document.createElement("div");
  toast.className = "jm-toast"; toast.setAttribute("role", "status"); toast.setAttribute("aria-live", "polite");
  document.body.appendChild(toast);
  var toastTimer = null;
  function say(msg) {
    toast.textContent = msg; toast.classList.add("show");
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { toast.classList.remove("show"); }, 2200);
  }

  // ---------- per-entry controls ----------
  function ratingName(n) {
    return ({
      1: "F-tier · Replace",
      2: "B-tier · Reconsider",
      3: "A-tier · Keep",
      4: "S-tier · Life-changing · Celebrate"
    })[n] || "";
  }
  function parseRatingResponse(response) {
    return response.text().then(function (raw) {
      var data = {};
      try { data = raw ? JSON.parse(raw) : {}; } catch (e) {
        throw new Error("non-JSON response");
      }
      if (!response.ok || !data.ok) throw new Error(data.error || ("HTTP " + response.status));
      return data;
    });
  }
  function paintRatingButtons(buttons, value) {
    buttons.forEach(function (button) {
      button.setAttribute("aria-pressed", String(Number(button.dataset.rating) === Number(value)));
    });
  }
  function renderRatingSummary(summaryEl, data) {
    while (summaryEl.firstChild) summaryEl.removeChild(summaryEl.firstChild);
    if (!data || !data.total) {
      summaryEl.textContent = "No semester ratings yet.";
      return;
    }
    var count = document.createElement("span");
    count.textContent = data.total + (data.total === 1 ? " response" : " responses");
    summaryEl.appendChild(count);

    var chart = document.createElement("span");
    chart.className = "jm-rating-histogram";
    var yAxis = document.createElement("span");
    yAxis.className = "jm-rating-y-axis";
    yAxis.setAttribute("aria-hidden", "true");
    [100, 50, 0].forEach(function (value) {
      var yTick = document.createElement("span");
      yTick.className = "jm-rating-y-tick";
      yTick.textContent = value;
      yAxis.appendChild(yTick);
    });

    var plot = document.createElement("span");
    plot.className = "jm-rating-plot";
    var xAxis = document.createElement("span");
    xAxis.className = "jm-rating-x-axis";
    var labels = [];
    [1, 2, 3, 4].forEach(function (rating) {
      var bin = document.createElement("span");
      bin.className = "jm-rating-bin";
      var segment = document.createElement("span");
      var n = Number(data.counts && data.counts[rating]) || 0;
      var pct = Number(data.percentages && data.percentages[rating]) || 0;
      segment.className = "jm-rating-bar jm-rating-" + rating;
      segment.style.height = pct ? Math.max(2, pct) + "%" : "0";
      segment.title = ratingName(rating) + ": " + n;
      bin.appendChild(segment);
      plot.appendChild(bin);

      var xTick = document.createElement("span");
      xTick.className = "jm-rating-x-tick";
      xTick.textContent = rating;
      xAxis.appendChild(xTick);
      labels.push(rating + ": " + n + " (" + Math.round(pct) + "%)");
    });
    chart.appendChild(yAxis);
    chart.appendChild(plot);
    chart.appendChild(xAxis);
    chart.setAttribute("role", "img");
    chart.setAttribute("aria-label", labels.join(", ") + ". X-axis: rating. Y-axis: percent of responses.");
    summaryEl.appendChild(chart);

    if (data.yourRating) {
      var yours = document.createElement("span");
      yours.className = "jm-rating-yours";
      yours.textContent = "You: " + data.yourRating;
      summaryEl.appendChild(yours);
    }
  }
  function ratingUrl(params) {
    var endpoint = cfg.ratingsEndpoint || "/api/ratings";
    var query = Object.keys(params).map(function (key) {
      return encodeURIComponent(key) + "=" + encodeURIComponent(params[key]);
    }).join("&");
    return endpoint + (endpoint.indexOf("?") === -1 ? "?" : "&") + query;
  }

  function paintSavedRatings(data) {
    var ratings = data && data.ratings || {};
    Object.keys(ratings).forEach(function (id) {
      var el = byId[id];
      if (!el) return;
      var buttons = Array.prototype.slice.call(el.querySelectorAll("[data-ratings] [data-rating]"));
      paintRatingButtons(buttons, ratings[id]);
    });
    return Object.keys(ratings).length > 0;
  }

  function renderEntrySummary(el) {
    var summaryEl = el.querySelector(".jm-rating-summary");
    if (!summaryEl) return;
    summaryEl.textContent = summariesError
      ? "Ratings are unavailable right now."
      : "";
    if (!summariesError) renderRatingSummary(summaryEl, summaries[el.dataset.id] || null);
    summaryEl.classList.remove("jm-hidden");
    summaryEl.setAttribute("data-visible", "true");
  }

  function refreshVisibleSummaries() {
    entries.forEach(function (el) {
      var summaryEl = el.querySelector(".jm-rating-summary");
      if (summaryEl && summaryEl.getAttribute("data-visible") === "true") renderEntrySummary(el);
    });
  }

  function loadAllSummaries() {
    if (summariesPromise) return summariesPromise;
    summariesError = false;
    summariesPromise = fetch(ratingUrl({ book: cfg.ratingsBook, all: "1" }), { credentials: "same-origin" })
      .then(parseRatingResponse)
      .then(function (data) {
        summaries = data && data.summaries || {};
      })
      .catch(function () {
        summariesError = true;
        say("Ratings are unavailable right now.");
      })
      .then(function () {
        summariesPromise = null;
      });
    return summariesPromise;
  }

  function viewVotes(el, button, summaryEl) {
    if (summaryEl.getAttribute("data-visible") === "true") {
      summaryEl.classList.add("jm-hidden");
      summaryEl.removeAttribute("data-visible");
      button.textContent = "Reveal";
      button.setAttribute("aria-label", "Reveal votes for this reading");
      return;
    }
    button.disabled = true;
    button.textContent = "Loading…";
    loadAllSummaries().then(function () {
      renderEntrySummary(el);
      button.disabled = false;
      button.textContent = "Hide votes";
      button.setAttribute("aria-label", "Hide votes for this reading");
    });
  }

  function hideEntryVotes(el) {
    var summaryEl = el.querySelector(".jm-rating-summary");
    if (summaryEl) {
      summaryEl.classList.add("jm-hidden");
      summaryEl.removeAttribute("data-visible");
    }
    var button = el.querySelector(".jm-view-votes");
    if (button) {
      button.disabled = false;
      button.textContent = "Reveal";
      button.setAttribute("aria-label", "Reveal votes for this reading");
    }
  }

  function revealAllVotes() {
    if (allVotesVisible) {
      entries.forEach(function (el) {
        el.open = false;
        hideEntryVotes(el);
      });
      allVotesVisible = false;
      if (revealButton) {
        revealButton.disabled = false;
        revealButton.textContent = "Reveal all votes";
      }
      return;
    }
    if (revealButton) {
      revealButton.disabled = true;
      revealButton.textContent = "Loading…";
    }
    loadAllSummaries().then(function () {
      entries.forEach(function (el) {
        el.open = true;
        renderEntrySummary(el);
        var button = el.querySelector(".jm-view-votes");
        if (button) {
          button.disabled = false;
          button.textContent = "Hide votes";
          button.setAttribute("aria-label", "Hide votes for this reading");
        }
      });
      allVotesVisible = true;
      if (revealButton) {
        revealButton.disabled = false;
        revealButton.textContent = "Hide all votes";
      }
    });
  }

  if (revealButton) {
    revealButton.classList.remove("jm-hidden");
    revealButton.removeAttribute("aria-hidden");
    revealButton.addEventListener("click", function () {
      revealAllVotes();
    });
  }

  entries.forEach(function (el) {
    var id = el.dataset.id;
    var titleLink = el.querySelector(".jm-entry-title a");
    var title = titleLink ? titleLink.textContent.trim() : id;
    var plan = el.querySelector("[data-actions]");
    var mine = plan && plan.querySelector('[data-choice="mine"]');
    var group = plan && plan.querySelector('[data-choice="group"]');
    var ratingCell = el.querySelector("[data-ratings]");
    var ratingButtons = ratingCell ? Array.prototype.slice.call(ratingCell.querySelectorAll("[data-rating]")) : [];
    var voteTools = el.querySelector(".jm-vote-tools");
    var viewVotesButton = el.querySelector(".jm-view-votes");
    var ratingSummaryEl = el.querySelector(".jm-rating-summary");
    if (!plan || !mine || !group || !ratingCell || ratingButtons.length !== 4 || !voteTools || !viewVotesButton || !ratingSummaryEl) return;

    function keepSummaryStill(event) {
      event.preventDefault();
      event.stopPropagation();
    }
    function paint() {
      var m = !!state.mine[id], g = !!state.group[id];
      mine.setAttribute("aria-pressed", String(m));
      group.setAttribute("aria-pressed", String(g));
      mine.textContent = "mine";
      group.textContent = "group";
      mine.title = m ? "Remove from my readings" : "Add to my readings";
      group.title = g ? "Remove from my group’s readings" : "My group has it";
      el.classList.toggle("is-mine", m);
      el.classList.toggle("is-group", g);
    }
    paint();
    if (titleLink) titleLink.addEventListener("click", function (event) { event.stopPropagation(); });
    mine.addEventListener("click", function (event) {
      keepSummaryStill(event);
      if (state.mine[id]) delete state.mine[id]; else state.mine[id] = true;
      paint(); save(); updateMeters(); applyFilters();
    });
    group.addEventListener("click", function (event) {
      keepSummaryStill(event);
      if (state.group[id]) delete state.group[id]; else state.group[id] = true;
      paint(); save(); applyFilters();
    });

    viewVotesButton.addEventListener("click", function (event) {
      keepSummaryStill(event);
      viewVotes(el, viewVotesButton, ratingSummaryEl);
    });

    var ratingBusy = false;
    ratingButtons.forEach(function (button) {
      button.addEventListener("click", function (event) {
        keepSummaryStill(event);
        saveRating(button.dataset.rating);
      });
    });
    function saveRating(value) {
      if (ratingBusy) return;
      ratingBusy = true;
      ratingButtons.forEach(function (button) { button.disabled = true; });
      ratingSummaryEl.textContent = "Saving…";
      fetch(cfg.ratingsEndpoint || "/api/ratings", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ book: cfg.ratingsBook, reading: id, rating: Number(value) })
      })
        .then(parseRatingResponse)
        .then(function (data) {
          renderRatingSummary(ratingSummaryEl, data);
          paintRatingButtons(ratingButtons, data.yourRating);
          loadAllSummaries().then(refreshVisibleSummaries);
          say("Saved. Thanks for the feedback.");
        })
        .catch(function () {
          ratingSummaryEl.textContent = "Ratings are unavailable right now.";
          say("Ratings are unavailable right now.");
        })
        .then(function () {
          ratingBusy = false;
          ratingButtons.forEach(function (button) { button.disabled = false; });
        });
    }
  });

  function loadExistingRatings() {
    fetch(ratingUrl({ book: cfg.ratingsBook, mine: "1" }), { credentials: "same-origin" })
      .then(parseRatingResponse)
      .then(function (data) {
        paintSavedRatings(data);
      })
      .catch(function () { /* Ratings are optional until a student submits one. */ });
  }
  loadExistingRatings();

  // ---------- meters ----------
  var barText = document.getElementById("jm-meter-text");
  var barFill = document.getElementById("jm-meter-fill");
  var scopeSelect = document.getElementById("jm-scope");
  function minutesIn(scopeId) {
    var total = 0;
    entries.forEach(function (el) {
      if (el.dataset.scopeId === scopeId && state.mine[el.dataset.id]) total += Number(el.dataset.min) || 0;
    });
    return total;
  }
  function fmt(m) {
    if (m < 60) return m + " min";
    var h = Math.floor(m / 60), r = m % 60;
    return h + " hr" + (r ? " " + r + " min" : "");
  }
  function updateMeters() {
    scopes.forEach(function (s) {
      var m = minutesIn(s.dataset.scope), t = targetOf(s.dataset.scope);
      var out = s.querySelector("[data-meter]");
      if (!out) return;
      out.textContent = m ? "You’ve picked " + fmt(m) + " of about " + fmt(t) + (m >= t ? " ✓" : "")
        : "Requirement: about " + fmt(t) + ". Nothing picked yet.";
      out.classList.toggle("met", m >= t);
    });
    if (scopeSelect && barText) {
      var cur = scopeSelect.value, m = minutesIn(cur), t = targetOf(cur);
      barText.textContent = fmt(m) + " of " + fmt(t) + (m >= t ? " ✓" : "");
      barText.classList.toggle("met", m >= t);
      barFill.style.width = Math.min(100, Math.round(m / t * 100)) + "%";
    }
  }
  if (scopeSelect) {
    scopeSelect.addEventListener("change", function () {
      updateMeters();
      var target = scopeById[scopeSelect.value];
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    // Follow the reader: the bar shows whichever week/unit is on screen.
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (items) {
        items.forEach(function (it) {
          if (it.isIntersecting && scopeSelect.value !== it.target.dataset.scope) {
            scopeSelect.value = it.target.dataset.scope; updateMeters();
          }
        });
      }, { rootMargin: "-80px 0px -70% 0px" });
      scopes.forEach(function (s) { io.observe(s); });
    }
  }

  // ---------- filters ----------
  var search = document.getElementById("jm-search");
  var countEl = document.getElementById("jm-count");
  var chips = Array.prototype.slice.call(document.querySelectorAll(".jm-chip"));
  function pressed(group) {
    return chips.filter(function (c) { return c.dataset.group === group && c.getAttribute("aria-pressed") === "true"; })
      .map(function (c) { return c.dataset.value; });
  }
  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      var on = c.getAttribute("aria-pressed") !== "true";
      if (c.dataset.single) {
        chips.forEach(function (o) { if (o.dataset.group === c.dataset.group) o.setAttribute("aria-pressed", "false"); });
      }
      c.setAttribute("aria-pressed", String(on));
      applyFilters();
    });
  });
  if (search) search.addEventListener("input", applyFilters);
  document.querySelectorAll(".jm-units-nav a").forEach(function (link) {
    link.addEventListener("click", function (event) {
      var target = document.getElementById(link.getAttribute("href").slice(1));
      if (!target) return;
      event.preventDefault();
      target.open = true;
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
  function lengthOk(min, band) {
    if (band === "short") return min <= 10;
    if (band === "medium") return min > 10 && min <= 25;
    if (band === "long") return min > 25;
    return true;
  }
  function applyFilters() {
    var q = search ? search.value.trim().toLowerCase() : "";
    var formats = pressed("format"), lengths = pressed("length"), stances = pressed("stance"), views = pressed("view");
    var shown = 0;
    entries.forEach(function (el) {
      var id = el.dataset.id, ok = true;
      if (q && el.dataset.search.indexOf(q) === -1) ok = false;
      if (ok && formats.length && formats.indexOf(el.dataset.format) === -1) ok = false;
      if (ok && lengths.length && !lengths.some(function (b) { return lengthOk(Number(el.dataset.min), b); })) ok = false;
      if (ok && stances.length && stances.indexOf(el.dataset.stance || "none") === -1) ok = false;
      if (ok && views.indexOf("mine") !== -1 && !state.mine[id]) ok = false;
      if (ok && views.indexOf("open") !== -1 && (state.group[id] || state.mine[id])) ok = false;
      el.classList.toggle("jm-hidden", !ok);
      if (ok) shown++;
    });
    document.querySelectorAll(".jm-week").forEach(function (w) {
      w.classList.toggle("jm-hidden", !w.querySelector(".jm-entry:not(.jm-hidden)"));
    });
    document.querySelectorAll(".jm-unit").forEach(function (u) {
      var hasVisible = !!u.querySelector(".jm-entry:not(.jm-hidden)");
      u.classList.toggle("jm-hidden", !hasVisible);
      if (hasVisible && (q || formats.length || lengths.length || stances.length || views.length)) u.open = true;
    });
    if (countEl) {
      countEl.textContent = shown === entries.length ? "Showing all " + entries.length + " readings"
        : "Showing " + shown + " of " + entries.length + " readings";
    }
  }

  // ---------- copy my list ----------
  var copyBtn = document.getElementById("jm-copy");
  if (copyBtn) copyBtn.addEventListener("click", function () {
    var lines = [cfg.menuTitle + " — my readings", ""];
    var any = false;
    scopes.forEach(function (s) {
      var picked = entries.filter(function (el) { return el.dataset.scopeId === s.dataset.scope && state.mine[el.dataset.id]; });
      if (!picked.length) return;
      any = true;
      lines.push(s.dataset.scopeLabel + " (" + fmt(minutesIn(s.dataset.scope)) + " picked)");
      picked.forEach(function (el) {
        var a = el.querySelector(".jm-entry-title a");
        lines.push("• " + a.textContent.trim() + " (~" + el.dataset.min + " min)");
        lines.push("  " + a.href);
      });
      lines.push("");
    });
    if (!any) { say("Pick a reading first, then copy your list."); return; }
    var text = lines.join("\n");
    function fallback() {
      var t = document.createElement("textarea"); t.value = text; t.setAttribute("readonly", "");
      t.style.position = "fixed"; t.style.opacity = "0"; document.body.appendChild(t); t.select();
      var ok = false; try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
      document.body.removeChild(t);
      say(ok ? "Copied. Paste it wherever you need it." : "Couldn’t copy here. Try another browser.");
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { say("Copied. Paste it wherever you need it."); }, fallback);
    } else fallback();
  });

  // ---------- clear (two clicks, no pop-up) ----------
  var clearBtn = document.getElementById("jm-clear");
  var armed = null;
  if (clearBtn) clearBtn.addEventListener("click", function () {
    if (!armed) {
      clearBtn.textContent = "Click again to clear";
      armed = setTimeout(function () { clearBtn.textContent = "Clear my picks"; armed = null; }, 4000);
      return;
    }
    clearTimeout(armed); armed = null; clearBtn.textContent = "Clear my picks";
    state.mine = {}; state.group = {};
    save();
    entries.forEach(function (el) {
      el.classList.remove("is-mine", "is-group");
      el.querySelectorAll(".jm-btn-mine, .jm-btn-group").forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
      el.querySelector(".jm-btn-mine").textContent = "mine";
      el.querySelector(".jm-btn-mine").title = "Add to my readings";
      el.querySelector(".jm-btn-group").textContent = "group";
      el.querySelector(".jm-btn-group").title = "My group has it";
    });
    updateMeters(); applyFilters();
    say("Picks cleared.");
  });

  document.documentElement.classList.add("jm-js");
  var tools = document.querySelectorAll(".jm-needs-js");
  Array.prototype.forEach.call(tools, function (t) { t.classList.remove("jm-hidden"); });
  updateMeters(); applyFilters();
})();
