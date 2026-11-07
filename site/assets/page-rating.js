/* Anonymous page ratings with optional quality dimensions. */
(function () {
  "use strict";

  var scoreLabels = {
    clarity: {
      1: "Very hard to follow",
      2: "Hard to follow",
      3: "Mostly understandable",
      4: "Easy to follow",
      5: "Very clear"
    },
    practice: {
      1: "Not enough",
      2: "A little short",
      3: "About right",
      4: "More than enough",
      5: "More than needed"
    },
    polish: {
      1: "Several glitches or rough spots",
      2: "Some noticeable rough spots",
      3: "Mostly fine",
      4: "Worked smoothly",
      5: "Polished and worked smoothly"
    }
  };

  function init(root) {
    var book = root.getAttribute("data-book");
    var page = root.getAttribute("data-page");
    var endpoint = root.getAttribute("data-endpoint") || "/api/ratings";
    var reading = "page-" + page;
    var subject = /^chapter/i.test(page) ? "chapter" : "page";
    var overlay = document.createElement("div");

    overlay.className = "etb-page-rating-overlay";
    overlay.innerHTML = [
      '<div class="etb-page-rating-dialog" role="dialog" aria-modal="true" aria-labelledby="etb-page-rating-title">',
      '<button type="button" class="etb-page-rating-close" data-page-rating-close aria-label="Close">&times;</button>',
      '<h3 id="etb-page-rating-title">Rate this ' + subject + '</h3>',
      '<p class="etb-page-rating-sub">Your anonymous feedback helps improve the book.</p>',
      '<div class="etb-page-rating-options" role="group" aria-label="Overall usefulness, from 1 to 4">',
      '<button type="button" class="etb-page-rating-option" data-page-rating-value="1" aria-pressed="false" aria-label="1, not useful">1</button>',
      '<button type="button" class="etb-page-rating-option" data-page-rating-value="2" aria-pressed="false" aria-label="2, needs work">2</button>',
      '<button type="button" class="etb-page-rating-option" data-page-rating-value="3" aria-pressed="false" aria-label="3, useful">3</button>',
      '<button type="button" class="etb-page-rating-option" data-page-rating-value="4" aria-pressed="false" aria-label="4, very useful">4</button>',
      '</div>',
      '<div class="etb-page-rating-scale"><span>1 Not useful</span><span>4 Very useful</span></div>',
      '<section class="etb-page-rating-dimensions" aria-labelledby="etb-page-rating-details-title">',
      '<h4 id="etb-page-rating-details-title">More specific feedback <span>(optional)</span></h4>',
      '<p class="etb-page-rating-dimensions-intro">Move any slider you want to rate. You can leave the rest blank.</p>',
      '<div class="etb-page-rating-dimension">',
      '<label class="etb-page-rating-dimension-label" for="etb-page-rating-clarity">How easy was this ' + subject + ' to understand?</label>',
      '<div class="etb-page-rating-range-labels"><span>Hard to follow</span><span>Very clear</span></div>',
      '<input class="etb-page-rating-range" id="etb-page-rating-clarity" data-page-rating-dimension="clarity" type="range" min="1" max="5" step="1" value="3" aria-valuetext="Not rated">',
      '<output class="etb-page-rating-output" data-page-rating-output="clarity" for="etb-page-rating-clarity">Not rated</output>',
      '</div>',
      '<div class="etb-page-rating-dimension">',
      '<label class="etb-page-rating-dimension-label" for="etb-page-rating-practice">Did this ' + subject + ' give you enough practice?</label>',
      '<div class="etb-page-rating-range-labels"><span>Not enough</span><span>More than enough</span></div>',
      '<input class="etb-page-rating-range" id="etb-page-rating-practice" data-page-rating-dimension="practice" type="range" min="1" max="5" step="1" value="3" aria-valuetext="Not rated">',
      '<output class="etb-page-rating-output" data-page-rating-output="practice" for="etb-page-rating-practice">Not rated</output>',
      '<label class="etb-page-rating-na"><input type="checkbox" data-page-rating-practice-na> This page did not include practice</label>',
      '</div>',
      '<div class="etb-page-rating-dimension">',
      '<label class="etb-page-rating-dimension-label" for="etb-page-rating-polish">How polished and reliable did this ' + subject + ' feel?</label>',
      '<div class="etb-page-rating-range-labels"><span>Glitchy or rough</span><span>Polished and smooth</span></div>',
      '<input class="etb-page-rating-range" id="etb-page-rating-polish" data-page-rating-dimension="polish" type="range" min="1" max="5" step="1" value="3" aria-valuetext="Not rated">',
      '<output class="etb-page-rating-output" data-page-rating-output="polish" for="etb-page-rating-polish">Not rated</output>',
      '</div>',
      '</section>',
      '<label class="etb-page-rating-comment-label" for="etb-page-rating-comment">What did you love about this ' + subject + '? <span>(optional)</span></label>',
      '<textarea class="etb-page-rating-comment" id="etb-page-rating-comment" maxlength="1000" placeholder="A sentence or two is plenty."></textarea>',
      '<label class="etb-page-rating-comment-label" for="etb-page-rating-improvement">What is one thing we can improve? <span>(optional)</span></label>',
      '<textarea class="etb-page-rating-comment" id="etb-page-rating-improvement" maxlength="1000" placeholder="A sentence or two is plenty."></textarea>',
      '<p class="etb-page-rating-status" data-page-rating-status aria-live="polite">Choose an overall rating to save.</p>',
      '<div class="etb-page-rating-actions">',
      '<button type="button" class="etb-page-rating-cancel" data-page-rating-close>Cancel</button>',
      '<button type="button" class="etb-page-rating-submit" data-page-rating-submit disabled>Save rating</button>',
      '</div>',
      '</div>'
    ].join("");

    document.body.appendChild(overlay);

    var options = Array.prototype.slice.call(overlay.querySelectorAll("[data-page-rating-value]"));
    var sliders = {};
    Array.prototype.forEach.call(overlay.querySelectorAll("[data-page-rating-dimension]"), function (input) {
      sliders[input.getAttribute("data-page-rating-dimension")] = input;
    });
    var outputs = {};
    Array.prototype.forEach.call(overlay.querySelectorAll("[data-page-rating-output]"), function (output) {
      outputs[output.getAttribute("data-page-rating-output")] = output;
    });

    var status = overlay.querySelector("[data-page-rating-status]");
    var submit = overlay.querySelector("[data-page-rating-submit]");
    var commentBox = overlay.querySelector("#etb-page-rating-comment");
    var improvementBox = overlay.querySelector("#etb-page-rating-improvement");
    var practiceNA = overlay.querySelector("[data-page-rating-practice-na]");
    var selectedRating = null;
    var busy = false;
    var touchedAny = false;
    var lastFocus = null;
    var rate = null;

    function setRating(value) {
      selectedRating = value ? Number(value) : null;
      options.forEach(function (button) {
        button.setAttribute("aria-pressed", String(Number(button.getAttribute("data-page-rating-value")) === selectedRating));
      });
      submit.disabled = !selectedRating || busy;
    }

    function isRated(name) {
      return sliders[name].getAttribute("data-rated") === "true";
    }

    function setSlider(name, value, rated) {
      var input = sliders[name];
      var output = outputs[name];
      if (value !== null && value !== undefined && value !== "") input.value = String(value);
      input.setAttribute("data-rated", rated ? "true" : "false");
      if (name === "practice" && practiceNA.checked) {
        input.disabled = true;
        input.setAttribute("aria-valuetext", "Not applicable");
        output.textContent = "Not applicable";
        return;
      }
      input.disabled = false;
      if (rated) {
        var label = scoreLabels[name][Number(input.value)];
        input.setAttribute("aria-valuetext", input.value + " out of 5, " + label);
        output.textContent = input.value + " — " + label;
      } else {
        input.setAttribute("aria-valuetext", "Not rated");
        output.textContent = "Not rated";
      }
    }

    function refreshPractice() {
      setSlider("practice", sliders.practice.value, isRated("practice"));
    }

    function paint(record) {
      if (!record) return;
      setRating(record.rating);
      ["clarity", "practice", "polish"].forEach(function (name) {
        var value = record[name];
        setSlider(name, value, value !== null && value !== undefined);
      });
      practiceNA.checked = record.practice_na === true || Number(record.practice_na) === 1;
      refreshPractice();
      commentBox.value = record.comment || "";
      improvementBox.value = record.improvement || "";
    }

    function updateRange(name) {
      sliders[name].setAttribute("data-rated", "true");
      setSlider(name, sliders[name].value, true);
    }

    function open() {
      lastFocus = document.activeElement;
      overlay.classList.add("is-open");
      document.documentElement.style.overflow = "hidden";
      var selected = options.filter(function (button) {
        return button.getAttribute("aria-pressed") === "true";
      })[0];
      (selected || options[0]).focus();
    }

    function close() {
      overlay.classList.remove("is-open");
      document.documentElement.style.overflow = "";
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    function parse(response) {
      if (!response.ok) throw new Error("rating request failed");
      return response.json();
    }

    function mount() {
      var target = document.querySelector(".etb-nav-inner");
      if (!target) return;
      if (rate && rate.parentNode === target) return;
      if (rate && rate.parentNode) rate.parentNode.removeChild(rate);
      rate = document.createElement("button");
      rate.type = "button";
      rate.className = "etb-nav-rate";
      rate.setAttribute("aria-label", "Rate this " + subject);
      rate.textContent = "Rate";
      target.insertBefore(rate, target.lastElementChild);
      rate.addEventListener("click", open);
    }

    fetch(endpoint + "?book=" + encodeURIComponent(book) + "&mine=1", { credentials: "same-origin" })
      .then(parse)
      .then(function (data) {
        var saved = data && data.ratings && data.ratings[reading];
        if (saved && !touchedAny) paint(saved);
      })
      .catch(function () {});

    options.forEach(function (button) {
      button.addEventListener("click", function () {
        if (busy) return;
        touchedAny = true;
        setRating(button.getAttribute("data-page-rating-value"));
        status.textContent = "Add any optional details, then save.";
      });
    });

    ["clarity", "practice", "polish"].forEach(function (name) {
      sliders[name].addEventListener("input", function () {
        if (busy) return;
        touchedAny = true;
        updateRange(name);
      });
    });

    practiceNA.addEventListener("change", function () {
      if (busy) return;
      touchedAny = true;
      refreshPractice();
    });

    commentBox.addEventListener("input", function () { touchedAny = true; });
    improvementBox.addEventListener("input", function () { touchedAny = true; });

    submit.addEventListener("click", function () {
      if (busy) return;
      if (!selectedRating) {
        status.textContent = "Choose an overall rating first.";
        options[0].focus();
        return;
      }

      busy = true;
      submit.disabled = true;
      status.textContent = "Saving…";
      var payload = {
        book: book,
        reading: reading,
        rating: selectedRating,
        clarity: isRated("clarity") ? Number(sliders.clarity.value) : null,
        practice: practiceNA.checked ? null : (isRated("practice") ? Number(sliders.practice.value) : null),
        practice_na: practiceNA.checked,
        polish: isRated("polish") ? Number(sliders.polish.value) : null,
        comment: commentBox.value.trim(),
        improvement: improvementBox.value.trim()
      };

      fetch(endpoint, {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }).then(parse).then(function (data) {
        if (data && data.yourRating) setRating(data.yourRating);
        if (data && data.preview) {
          status.textContent = "Preview only — nothing was saved to the live database.";
        } else {
          status.textContent = "Saved. Thanks.";
        }
      }).catch(function () {
        status.textContent = "Ratings are unavailable right now.";
      }).then(function () {
        busy = false;
        submit.disabled = !selectedRating;
      });
    });

    Array.prototype.forEach.call(overlay.querySelectorAll("[data-page-rating-close]"), function (button) {
      button.addEventListener("click", close);
    });
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) close();
    });
    overlay.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        close();
        return;
      }
      if (event.key !== "Tab") return;
      var focusable = Array.prototype.filter.call(
        overlay.querySelectorAll("button:not([disabled]), input:not([disabled]), textarea"),
        function (item) { return item.offsetParent !== null; }
      );
      if (!focusable.length) return;
      if (event.shiftKey && document.activeElement === focusable[0]) {
        focusable[focusable.length - 1].focus();
        event.preventDefault();
      } else if (!event.shiftKey && document.activeElement === focusable[focusable.length - 1]) {
        focusable[0].focus();
        event.preventDefault();
      }
    });

    mount();
    if (window.MutationObserver) {
      var observer = new MutationObserver(mount);
      observer.observe(document.body, { childList: true, subtree: true });
    }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
    setTimeout(function () {
      if (!document.querySelector(".etb-nav-inner")) {
        var fallback = document.createElement("button");
        fallback.type = "button";
        fallback.className = "etb-page-rating-fallback";
        fallback.setAttribute("aria-label", "Rate this " + subject);
        fallback.textContent = "Rate";
        fallback.addEventListener("click", open);
        document.body.appendChild(fallback);
      }
    }, 1000);
  }

  document.querySelectorAll("[data-page-rating]").forEach(init);
})();