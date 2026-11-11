/* The Question Board — small, optional enhancements. The site works without them. */
(function () {
  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  var links = document.getElementById("nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      links.classList.toggle("is-open", !open);
    });
  }

  // Board filters: keep only the chosen field's cards, in place
  var buttons = document.querySelectorAll(".filter[data-filter]");
  var cards = document.querySelectorAll("#board-cards > li[data-card-field]");
  var status = document.getElementById("filter-status");
  if (!buttons.length || !cards.length) return;

  function apply(field, updateUrl) {
    var shown = 0;
    buttons.forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.filter === field));
    });
    cards.forEach(function (li) {
      var match = field === "all" || li.dataset.cardField === field;
      li.hidden = !match;
      if (match) shown++;
    });
    if (status) {
      var label = field === "all" ? "all fields" : document.querySelector('.filter[data-filter="' + field + '"]').textContent.trim();
      status.textContent = "Showing " + shown + (shown === 1 ? " question" : " questions") + " in " + label + ".";
    }
    if (updateUrl && window.history && history.replaceState) {
      try {
        var u = new URL(window.location.href);
        if (field === "all") u.searchParams.delete("field"); else u.searchParams.set("field", field);
        history.replaceState(null, "", u.toString());
      } catch (e) { /* some embedded viewers do not allow this; the filter still works */ }
    }
  }

  buttons.forEach(function (b) {
    b.addEventListener("click", function () { apply(b.dataset.filter, true); });
  });

  var start = new URLSearchParams(window.location.search).get("field");
  if (start && document.querySelector('.filter[data-filter="' + start + '"]')) apply(start, false);
})();
