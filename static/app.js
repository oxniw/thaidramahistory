// ==============================================================================
// File: .//Description-of-file/frontend.md
// Overview: Read-only notice board client with safe DOM rendering and filtering
// ==============================================================================

(function () {
  "use strict";

  // Application State
  const state = {
    notices: [],
    filter: "all",
    search: "",
  };

  // DOM Elements
  const noticesGrid = document.getElementById("notices-grid");
  const emptyState = document.getElementById("empty-state");
  const searchInput = document.getElementById("search-input");
  const searchClearBtn = document.getElementById("search-clear-btn");
  const filterTabs = document.getElementById("filter-tabs");

  // Counters
  const countAll = document.getElementById("count-all");
  const countPinned = document.getElementById("count-pinned");
  const countUrgent = document.getElementById("count-urgent");

  // Format Timestamps
  function formatDate(isoString) {
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
    } catch {
      return isoString;
    }
  }

  // Fetch notices from API
  async function fetchNotices() {
    try {
      const params = new URLSearchParams();
      if (state.search) params.append("search", state.search);

      const res = await fetch(`/api/notices?${params.toString()}`);
      if (!res.ok) throw new Error("Failed to load notices");
      state.notices = await res.json();
      updateCounters();
      renderBoard();
    } catch (err) {
      console.error("Notice fetch error:", err);
    }
  }

  // Update summary counts
  function updateCounters() {
    countAll.textContent = state.notices.length;
    countPinned.textContent = state.notices.filter((n) => n.is_pinned).length;
    countUrgent.textContent = state.notices.filter((n) => n.priority === "urgent").length;
  }

  // Filter notices for display
  function getFilteredNotices() {
    let list = state.notices;

    if (state.filter === "pinned") {
      list = list.filter((n) => n.is_pinned);
    } else if (state.filter === "urgent") {
      list = list.filter((n) => n.priority === "urgent");
    }

    return list;
  }

  // Construct Safe Notice DOM Node (prevents XSS)
  function createNoticeCardElement(notice) {
    const card = document.createElement("article");
    card.className = "notice-card";
    if (notice.is_pinned) card.classList.add("pinned");
    if (notice.priority === "urgent") card.classList.add("urgent");

    // Header
    const cardHeader = document.createElement("div");
    cardHeader.className = "card-header";

    const badgeGroup = document.createElement("div");
    badgeGroup.className = "badge-group";

    if (notice.is_pinned) {
      const pinBadge = document.createElement("span");
      pinBadge.className = "badge badge-pinned";
      pinBadge.textContent = "PINNED";
      badgeGroup.appendChild(pinBadge);
    }

    if (notice.priority === "urgent") {
      const urgentBadge = document.createElement("span");
      urgentBadge.className = "badge badge-urgent";
      urgentBadge.textContent = "URGENT";
      badgeGroup.appendChild(urgentBadge);
    }

    const catBadge = document.createElement("span");
    catBadge.className = "badge badge-category";
    catBadge.textContent = notice.category || "General";
    badgeGroup.appendChild(catBadge);

    const dateSpan = document.createElement("span");
    dateSpan.className = "card-date";
    dateSpan.textContent = formatDate(notice.created_at);

    cardHeader.appendChild(badgeGroup);
    cardHeader.appendChild(dateSpan);

    // Body
    const cardBody = document.createElement("div");
    cardBody.className = "card-body";

    const titleEl = document.createElement("h2");
    titleEl.className = "card-title";
    titleEl.textContent = notice.title;

    const contentEl = document.createElement("p");
    contentEl.className = "card-text";
    contentEl.textContent = notice.content;

    cardBody.appendChild(titleEl);
    cardBody.appendChild(contentEl);

    // Footer
    const cardFooter = document.createElement("div");
    cardFooter.className = "card-footer";

    const authorSpan = document.createElement("span");
    authorSpan.className = "card-author";
    authorSpan.textContent = `POSTED BY: ${notice.author || "Staff"}`;
    cardFooter.appendChild(authorSpan);

    card.appendChild(cardHeader);
    card.appendChild(cardBody);
    card.appendChild(cardFooter);
    return card;
  }

  // Render notice board cards
  function renderBoard() {
    const list = getFilteredNotices();
    noticesGrid.innerHTML = "";

    if (list.length === 0) {
      emptyState.style.display = "block";
      noticesGrid.style.display = "none";
    } else {
      emptyState.style.display = "none";
      noticesGrid.style.display = "grid";
      list.forEach((item) => {
        noticesGrid.appendChild(createNoticeCardElement(item));
      });
    }
  }

  // Filter Tabs Event
  filterTabs.addEventListener("click", (e) => {
    const tab = e.target.closest(".tab");
    if (!tab) return;
    filterTabs.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");
    state.filter = tab.dataset.filter;
    renderBoard();
  });

  // Search Event
  let searchTimeout = null;
  searchInput.addEventListener("input", (e) => {
    const val = e.target.value;
    searchClearBtn.style.display = val ? "inline-block" : "none";
    if (searchTimeout) clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      state.search = val.trim();
      fetchNotices();
    }, 250);
  });

  searchClearBtn.addEventListener("click", () => {
    searchInput.value = "";
    state.search = "";
    searchClearBtn.style.display = "none";
    fetchNotices();
  });

  // Initial load
  fetchNotices();
})();
