// ==============================================================================
// File: .//Description-of-file/program_frontend.md
// Overview: Database control portal controller with split table and live editor
// ==============================================================================

(function () {
  "use strict";

  let records = [];
  let editingId = null;
  let currentSort = "default";

  // Elements
  const recordsTbody = document.getElementById("records-tbody");
  const recordCount = document.getElementById("record-count");
  const emptyState = document.getElementById("empty-state");
  const filterSearch = document.getElementById("filter-search");
  const managerSortSelect = document.getElementById("manager-sort-select");
  const exportBtn = document.getElementById("export-btn");
  const importBtn = document.getElementById("import-btn");
  const importFileInput = document.getElementById("import-file-input");
  const newRecordBtn = document.getElementById("new-record-btn");

  // Form Elements
  const recordForm = document.getElementById("record-form");
  const formId = document.getElementById("form-id");
  const formTitle = document.getElementById("form-title");
  const formCategory = document.getElementById("form-category");
  const formPriority = document.getElementById("form-priority");
  const formAuthor = document.getElementById("form-author");
  const formPinned = document.getElementById("form-pinned");
  const formContent = document.getElementById("form-content");
  const resetBtn = document.getElementById("reset-btn");
  const editorTitle = document.getElementById("editor-title");
  const editorModeBadge = document.getElementById("editor-mode-badge");
  const toast = document.getElementById("toast");

  let toastTimer = null;
  function showToast(message, isError = false) {
    if (toastTimer) clearTimeout(toastTimer);
    toast.textContent = message;
    toast.className = isError ? "toast active error" : "toast active";
    toastTimer = setTimeout(() => {
      toast.className = "toast";
    }, 3500);
  }

  function formatDate(isoString) {
    if (!isoString) return "";
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
    } catch {
      return isoString;
    }
  }

  // Fetch all notices from manager API
  async function loadNotices() {
    try {
      const res = await fetch(`/api/notices?sort_by=${currentSort}`);
      if (!res.ok) throw new Error("Failed to load records from database.");
      records = await res.json();
      renderTable();
    } catch (err) {
      console.error(err);
      showToast(err.message, true);
    }
  }

  // Render Table Rows
  function renderTable() {
    const search = filterSearch.value.trim().toLowerCase();
    const filtered = records.filter((r) => {
      if (!search) return true;
      return (
        (r.title && r.title.toLowerCase().includes(search)) ||
        (r.author && r.author.toLowerCase().includes(search)) ||
        (r.category && r.category.toLowerCase().includes(search))
      );
    });

    recordCount.textContent = filtered.length;
    recordsTbody.innerHTML = "";

    if (filtered.length === 0) {
      emptyState.style.display = "block";
      return;
    }
    emptyState.style.display = "none";

    filtered.forEach((item) => {
      const tr = document.createElement("tr");

      // Tags Cell
      const tagsTd = document.createElement("td");
      if (item.is_pinned) {
        const pinSpan = document.createElement("span");
        pinSpan.className = "badge-tag pin";
        pinSpan.textContent = "PIN";
        tagsTd.appendChild(pinSpan);
      }
      if (item.priority === "urgent") {
        const urgSpan = document.createElement("span");
        urgSpan.className = "badge-tag urg";
        urgSpan.textContent = "URG";
        tagsTd.appendChild(urgSpan);
      }
      tr.appendChild(tagsTd);

      // Title Cell
      const titleTd = document.createElement("td");
      titleTd.className = "table-title";
      titleTd.textContent = item.title;
      tr.appendChild(titleTd);

      // Category Cell
      const catTd = document.createElement("td");
      catTd.textContent = item.category || "General";
      tr.appendChild(catTd);

      // Date Cell
      const dateTd = document.createElement("td");
      dateTd.textContent = formatDate(item.created_at);
      tr.appendChild(dateTd);

      // Actions Cell
      const actionsTd = document.createElement("td");
      actionsTd.style.textAlign = "right";

      const editBtn = document.createElement("button");
      editBtn.className = "btn-action";
      editBtn.textContent = "EDIT";
      editBtn.style.marginRight = "0.3rem";
      editBtn.addEventListener("click", () => populateForm(item));

      const delBtn = document.createElement("button");
      delBtn.className = "btn-action";
      delBtn.textContent = "DEL";
      delBtn.addEventListener("click", () => deleteRecord(item.id));

      actionsTd.appendChild(editBtn);
      actionsTd.appendChild(delBtn);
      tr.appendChild(actionsTd);

      recordsTbody.appendChild(tr);
    });
  }

  // Populate Form for Editing
  function populateForm(item) {
    editingId = item.id;
    formId.value = item.id;
    formTitle.value = item.title;
    formCategory.value = item.category || "General";
    formPriority.value = item.priority || "normal";
    formAuthor.value = item.author || "Staff";
    formPinned.checked = Boolean(item.is_pinned);
    formContent.value = item.content;

    editorTitle.textContent = "EDIT RECORD";
    editorModeBadge.textContent = "EDIT";
    formTitle.focus();
  }

  // Reset Form to Create Mode
  function resetForm() {
    editingId = null;
    recordForm.reset();
    formId.value = "";
    formCategory.value = "General";
    formPriority.value = "normal";
    formAuthor.value = "Staff";
    formPinned.checked = false;

    editorTitle.textContent = "CREATE NOTICE";
    editorModeBadge.textContent = "NEW";
  }

  // Submit Handler (Create or Update)
  async function handleSubmit(e) {
    e.preventDefault();
    const payload = {
      title: formTitle.value.trim(),
      category: formCategory.value.trim() || "General",
      priority: formPriority.value,
      author: formAuthor.value.trim() || "Staff",
      is_pinned: formPinned.checked,
      content: formContent.value.trim(),
    };

    const isEdit = Boolean(editingId);
    const url = isEdit ? `/api/notices/${editingId}` : "/api/notices";
    const method = isEdit ? "PUT" : "POST";

    try {
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || "Database save failed.");
      }

      showToast(isEdit ? "Record updated in database." : "Record inserted into database.");
      resetForm();
      await loadNotices();
    } catch (err) {
      showToast(err.message, true);
    }
  }

  // Delete Record Handler
  async function deleteRecord(id) {
    if (!confirm("Permanently delete this notice from the database?")) return;

    try {
      const res = await fetch(`/api/notices/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Could not delete record from database.");

      showToast("Record deleted.");
      if (editingId === id) resetForm();
      await loadNotices();
    } catch (err) {
      showToast(err.message, true);
    }
  }

  // Export JSON Backup
  function handleExport() {
    window.location.href = "/api/export";
  }

  // Import JSON Backup
  async function handleImportFile(e) {
    const file = e.target.files[0];
    if (!file) return;

    try {
      const text = await file.text();
      const res = await fetch("/api/import", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: text,
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Import failed.");
      }

      const result = await res.json();
      showToast(result.message || "Import completed successfully.");
      importFileInput.value = "";
      await loadNotices();
    } catch (err) {
      showToast(err.message, true);
      importFileInput.value = "";
    }
  }

  // Event Listeners
  recordForm.addEventListener("submit", handleSubmit);
  resetBtn.addEventListener("click", resetForm);
  newRecordBtn.addEventListener("click", resetForm);
  filterSearch.addEventListener("input", renderTable);
  if (managerSortSelect) {
    managerSortSelect.addEventListener("change", (e) => {
      currentSort = e.target.value;
      loadNotices();
    });
  }
  exportBtn.addEventListener("click", handleExport);
  importBtn.addEventListener("click", () => importFileInput.click());
  importFileInput.addEventListener("change", handleImportFile);

  // Initial load
  loadNotices();
})();
