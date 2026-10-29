// ==============================================================================
// File: .//Description-of-file/frontend.md
// Overview: Client-side notice board controller with safe DOM rendering & admin flow
// ==============================================================================

(function () {
  "use strict";

  // Application State
  const state = {
    notices: [],
    filter: "all",
    search: "",
    adminKey: localStorage.getItem("bulletin_admin_key") || "",
    isAdmin: false,
    editingNoticeId: null,
  };

  // DOM Elements
  const noticesGrid = document.getElementById("notices-grid");
  const emptyState = document.getElementById("empty-state");
  const searchInput = document.getElementById("search-input");
  const searchClearBtn = document.getElementById("search-clear-btn");
  const filterTabs = document.getElementById("filter-tabs");
  const adminToggleBtn = document.getElementById("admin-toggle-btn");
  const adminStatusText = document.getElementById("admin-status-text");
  const createNoticeBtn = document.getElementById("create-notice-btn");
  const emptyCreateBtn = document.getElementById("empty-create-btn");
  const toast = document.getElementById("toast");

  // Admin Modal Elements
  const adminModal = document.getElementById("admin-modal");
  const adminModalClose = document.getElementById("admin-modal-close");
  const adminKeyInput = document.getElementById("admin-key-input");
  const adminSubmitBtn = document.getElementById("admin-submit-btn");
  const adminLogoutBtn = document.getElementById("admin-logout-btn");

  // Notice Form Modal Elements
  const noticeModal = document.getElementById("notice-modal");
  const noticeModalClose = document.getElementById("notice-modal-close");
  const noticeModalTitle = document.getElementById("notice-modal-title");
  const noticeForm = document.getElementById("notice-form");
  const noticeIdInput = document.getElementById("notice-id");
  const noticeTitleInput = document.getElementById("notice-title");
  const noticeCategoryInput = document.getElementById("notice-category");
  const noticePriorityInput = document.getElementById("notice-priority");
  const noticeAuthorInput = document.getElementById("notice-author");
  const noticePinnedInput = document.getElementById("notice-pinned");
  const noticeContentInput = document.getElementById("notice-content");
  const noticeCancelBtn = document.getElementById("notice-cancel-btn");

  // Counters
  const countAll = document.getElementById("count-all");
  const countPinned = document.getElementById("count-pinned");
  const countUrgent = document.getElementById("count-urgent");

  // Show Toast Message
  let toastTimer = null;
  function showToast(message, isError = false) {
    if (toastTimer) clearTimeout(toastTimer);
    toast.textContent = message;
    toast.className = isError ? "toast active error" : "toast active";
    toastTimer = setTimeout(() => {
      toast.className = "toast";
    }, 3500);
  }

  // Format Timestamps cleanly
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

  // Verify Admin Key with API
  async function checkAdminStatus(key) {
    if (!key) {
      setAdminState(false);
      return;
    }
    try {
      const res = await fetch("/api/auth/verify", {
        headers: { "X-Admin-Key": key },
      });
      if (res.ok) {
        state.adminKey = key;
        localStorage.setItem("bulletin_admin_key", key);
        setAdminState(true);
      } else {
        setAdminState(false);
        if (state.adminKey) {
          localStorage.removeItem("bulletin_admin_key");
          state.adminKey = "";
        }
      }
    } catch (err) {
      console.error("Auth check failed:", err);
      setAdminState(false);
    }
  }

  // Update UI based on Admin State
  function setAdminState(isAdmin) {
    state.isAdmin = isAdmin;
    if (isAdmin) {
      adminStatusText.textContent = "ADMIN ACTIVE";
      adminToggleBtn.classList.remove("btn-secondary");
      adminToggleBtn.classList.add("btn-primary");
      createNoticeBtn.style.display = "inline-flex";
      adminLogoutBtn.style.display = "inline-block";
    } else {
      adminStatusText.textContent = "ADMIN ACCESS";
      adminToggleBtn.classList.remove("btn-primary");
      adminToggleBtn.classList.add("btn-secondary");
      createNoticeBtn.style.display = "none";
      adminLogoutBtn.style.display = "none";
    }
    renderBoard();
  }

  // Fetch notices from FastAPI
  async function fetchNotices() {
    try {
      const params = new URLSearchParams();
      if (state.search) params.append("search", state.search);

      const res = await fetch(`/api/notices?${params.toString()}`);
      if (!res.ok) throw new Error("Failed to load notices from server");
      state.notices = await res.json();
      updateCounters();
      renderBoard();
    } catch (err) {
      console.error("Fetch error:", err);
      showToast("Cannot connect to server. Check database configuration.", true);
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

  // Construct Safe Notice DOM Node (prevents XSS vulnerabilities)
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
    authorSpan.textContent = `BY: ${notice.author || "Administration"}`;
    cardFooter.appendChild(authorSpan);

    // Admin Controls
    if (state.isAdmin) {
      const actionsGroup = document.createElement("div");
      actionsGroup.className = "card-actions";

      const pinBtn = document.createElement("button");
      pinBtn.className = "btn-card";
      pinBtn.textContent = notice.is_pinned ? "UNPIN" : "PIN";
      pinBtn.addEventListener("click", () => togglePinNotice(notice));

      const editBtn = document.createElement("button");
      editBtn.className = "btn-card";
      editBtn.textContent = "EDIT";
      editBtn.addEventListener("click", () => openEditModal(notice));

      const deleteBtn = document.createElement("button");
      deleteBtn.className = "btn-card";
      deleteBtn.textContent = "DELETE";
      deleteBtn.addEventListener("click", () => deleteNotice(notice.id));

      actionsGroup.appendChild(pinBtn);
      actionsGroup.appendChild(editBtn);
      actionsGroup.appendChild(deleteBtn);
      cardFooter.appendChild(actionsGroup);
    }

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

  // Open Create Modal
  function openCreateModal() {
    if (!state.isAdmin) {
      openAdminModal();
      return;
    }
    state.editingNoticeId = null;
    noticeModalTitle.textContent = "NEW NOTICE";
    noticeForm.reset();
    noticeIdInput.value = "";
    noticePriorityInput.value = "normal";
    noticeCategoryInput.value = "General";
    noticeAuthorInput.value = "Administration";
    noticePinnedInput.checked = false;
    noticeModal.style.display = "flex";
    noticeTitleInput.focus();
  }

  // Open Edit Modal
  function openEditModal(notice) {
    state.editingNoticeId = notice.id;
    noticeModalTitle.textContent = "EDIT NOTICE";
    noticeIdInput.value = notice.id;
    noticeTitleInput.value = notice.title;
    noticeCategoryInput.value = notice.category || "General";
    noticePriorityInput.value = notice.priority || "normal";
    noticeAuthorInput.value = notice.author || "Administration";
    noticePinnedInput.checked = Boolean(notice.is_pinned);
    noticeContentInput.value = notice.content;
    noticeModal.style.display = "flex";
    noticeTitleInput.focus();
  }

  // Save notice (Create or Update)
  async function handleNoticeSubmit(e) {
    e.preventDefault();
    const payload = {
      title: noticeTitleInput.value.trim(),
      content: noticeContentInput.value.trim(),
      category: noticeCategoryInput.value.trim() || "General",
      priority: noticePriorityInput.value,
      is_pinned: noticePinnedInput.checked,
      author: noticeAuthorInput.value.trim() || "Administration",
    };

    const isEdit = Boolean(state.editingNoticeId);
    const url = isEdit ? `/api/notices/${state.editingNoticeId}` : "/api/notices";
    const method = isEdit ? "PUT" : "POST";

    try {
      const res = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          "X-Admin-Key": state.adminKey,
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || "Server rejected request.");
      }

      noticeModal.style.display = "none";
      showToast(isEdit ? "Notice updated successfully." : "Notice published successfully.");
      await fetchNotices();
    } catch (err) {
      showToast(err.message, true);
    }
  }

  // Toggle Pinned Status
  async function togglePinNotice(notice) {
    try {
      const res = await fetch(`/api/notices/${notice.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-Admin-Key": state.adminKey,
        },
        body: JSON.stringify({ is_pinned: !notice.is_pinned }),
      });

      if (!res.ok) throw new Error("Failed to toggle pin status");
      showToast(notice.is_pinned ? "Notice unpinned." : "Notice pinned.");
      await fetchNotices();
    } catch (err) {
      showToast(err.message, true);
    }
  }

  // Delete Notice
  async function deleteNotice(noticeId) {
    if (!confirm("Are you sure you want to permanently delete this notice?")) return;

    try {
      const res = await fetch(`/api/notices/${noticeId}`, {
        method: "DELETE",
        headers: { "X-Admin-Key": state.adminKey },
      });

      if (!res.ok) throw new Error("Failed to delete notice");
      showToast("Notice deleted.");
      await fetchNotices();
    } catch (err) {
      showToast(err.message, true);
    }
  }

  // Admin Modal Handlers
  function openAdminModal() {
    adminKeyInput.value = state.adminKey || "";
    adminModal.style.display = "flex";
    adminKeyInput.focus();
  }

  async function handleAdminAuthSubmit() {
    const key = adminKeyInput.value.trim();
    if (!key) {
      showToast("Please enter an administrative key.", true);
      return;
    }
    try {
      const res = await fetch("/api/auth/verify", {
        headers: { "X-Admin-Key": key },
      });
      if (res.ok) {
        state.adminKey = key;
        localStorage.setItem("bulletin_admin_key", key);
        setAdminState(true);
        adminModal.style.display = "none";
        showToast("Admin credentials verified.");
      } else {
        showToast("Invalid administrative passkey.", true);
      }
    } catch (err) {
      showToast("Verification failed. Check network or server.", true);
    }
  }

  function handleAdminLogout() {
    state.adminKey = "";
    localStorage.removeItem("bulletin_admin_key");
    setAdminState(false);
    adminModal.style.display = "none";
    showToast("Admin passkey cleared.");
  }

  // Event Listeners
  filterTabs.addEventListener("click", (e) => {
    const tab = e.target.closest(".tab");
    if (!tab) return;
    filterTabs.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");
    state.filter = tab.dataset.filter;
    renderBoard();
  });

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

  adminToggleBtn.addEventListener("click", openAdminModal);
  adminModalClose.addEventListener("click", () => (adminModal.style.display = "none"));
  adminSubmitBtn.addEventListener("click", handleAdminAuthSubmit);
  adminLogoutBtn.addEventListener("click", handleAdminLogout);
  adminKeyInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") handleAdminAuthSubmit();
  });

  createNoticeBtn.addEventListener("click", openCreateModal);
  emptyCreateBtn.addEventListener("click", openCreateModal);
  noticeModalClose.addEventListener("click", () => (noticeModal.style.display = "none"));
  noticeCancelBtn.addEventListener("click", () => (noticeModal.style.display = "none"));
  noticeForm.addEventListener("submit", handleNoticeSubmit);

  // Close modals on clicking backdrop
  window.addEventListener("click", (e) => {
    if (e.target === adminModal) adminModal.style.display = "none";
    if (e.target === noticeModal) noticeModal.style.display = "none";
  });

  // Initialization
  if (state.adminKey) {
    checkAdminStatus(state.adminKey);
  }
  fetchNotices();
})();
