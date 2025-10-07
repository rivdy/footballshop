// ====================== products.js ======================
(function () {
  // ----- Ambil elemen utama -----
  const elList = qs("#product-list");
  const elLoading = qs("#state-loading");
  const elEmpty = qs("#state-empty");
  const elError = qs("#state-error");

  const btnRefresh = qs("#btn-refresh");
  const btnOpenCreate = qs("#btn-open-create");
  const btnOpenCreate2 = qs("#btn-open-create-2");

  // Modal Create/Edit
  const modal = qs("#modal-product");
  const form = qs("#form-product");
  const fId = qs("#f-id");
  const fName = qs("#f-name");
  const fPrice = qs("#f-price");
  const fCategory = qs("#f-category");
  const fDesc = qs("#f-description");
  const btnCancel = qs("#btn-cancel");
  const btnX = qs("#btn-x-close");        

  // Modal Delete
  const modalDel = qs("#modal-delete");
  const btnDelCancel = qs("#btn-del-cancel");
  const btnDelX = qs("#btn-del-x");  
  const btnDelYes = qs("#btn-del-yes");
  let pendingDeleteId = null;

  // Endpoints dari data-attributes
  const epEl = qs("#endpoints");
  if (!epEl) return;
  const EP = {
    list: epEl.dataset.list,
    create: epEl.dataset.create,
    updatePattern: epEl.dataset.updatePattern, // .../0/update/
    deletePattern: epEl.dataset.deletePattern, // .../0/delete/
  };

  // ----- Helper kecil -----
  function setState(state) {
    // 'loading' | 'empty' | 'error' | 'ok'
    if (!elList) return;
    hide(elLoading); hide(elEmpty); hide(elError); hide(elList);
    if (state === "loading") show(elLoading);
    else if (state === "empty") show(elEmpty);
    else if (state === "error") show(elError);
    else if (state === "ok") show(elList);
  }

  function placeholderImg() {
    return "https://placehold.co/600x450/0e0e16/8b5cf6?text=No+Image";
  }

  function detailUrl(id) {
    // rute kamu: /product/<int:id>/
    return `/product/${id}/`;
  }

  function buildUpdateUrl(id) {
    return buildUrlWithId(EP.updatePattern, id);
  }
  function buildDeleteUrl(id) {
    return buildUrlWithId(EP.deletePattern, id);
  }

  // ----- RENDER LIST -----
  function renderItems(items) {
    elList.innerHTML = "";
    for (const p of items) {
      const card = document.createElement("article");
      card.className = "card";
      card.dataset.id = p.id;

      card.innerHTML = `
        <div class="media">
          <img src="${p.thumbnail || placeholderImg()}" alt="${escapeHtml(p.name || "")}">
        </div>
        <h3 class="font-semibold text-lg mb-1">${escapeHtml(p.name || "")}</h3>
        <p class="text-sm opacity-85 mb-2">${escapeHtml(p.category || "")}</p>
        <div class="font-bold mb-3">Rp ${formatIDR(p.price || 0)}</div>

        <div class="flex gap-2 flex-wrap">
          <a class="btn" href="${detailUrl(p.id)}">Detail</a>
          <button class="btn btn-edit" data-id="${p.id}">✎ Edit</button>
          <button class="btn btn-del" data-id="${p.id}">🗑 Delete</button>
        </div>
      `;
      elList.appendChild(card);
    }

    // Bind tombol edit/delete
    qsa(".btn-edit", elList).forEach((b) => b.addEventListener("click", onEdit));
    qsa(".btn-del", elList).forEach((b) => b.addEventListener("click", onDelete));
  }

  // ----- LOAD LIST (AJAX) -----
  async function loadList() {
    try {
      setState("loading");
      // bawa filter aktif dari query string
      const url = new URL(EP.list, window.location.origin);
      const cur = new URLSearchParams(window.location.search);
      if (cur.get("filter")) url.searchParams.set("filter", cur.get("filter"));

      const json = await fetchJSON(url.toString());
      const items = Array.isArray(json.items) ? json.items : [];
      if (!items.length) {
        setState("empty");
        return;
      }
      renderItems(items);
      setState("ok");
    } catch (err) {
      console.error(err);
      setState("error");
      showToast("Gagal memuat data", "error");
    }
  }

  // ----- MODAL UTILS -----
    function openModal(){ if (modal) modal.classList.add('open'); }
    function closeModal(){ if (modal) modal.classList.remove('open'); form?.reset(); if (fId) fId.value=''; }

    function openDel(){ if (modalDel) modalDel.classList.add('open'); }
    function closeDel(){ if (modalDel) modalDel.classList.remove('open'); pendingDeleteId=null; }


  // Prefill form dari kartu (untuk edit cepat)
  function prefillFromCard(id) {
    const card = elList.querySelector(`.card [data-id="${id}"]`)?.closest(".card");
    if (!card) return;
    const name = card.querySelector("h3")?.textContent?.trim() || "";
    const priceText = card.querySelector(".font-bold")?.textContent || "";
    const price = (priceText.replace(/[^\d]/g, "")) || "0";
    const category = card.querySelector(".text-sm")?.textContent?.trim() || "";

    fId.value = id;
    fName.value = name;
    fPrice.value = price;
    fCategory.value = category;
    fDesc.value = ""; // deskripsi tidak ditampilkan pada kartu; biarkan kosong
  }

  // ----- ACTIONS -----
    function onCreate() {
    if (!form) return;
    form.reset();
    fId.value = "";
    const title = qs('#modal-product .modal-title');
    if (title) title.textContent = 'Create Product';  // ← judul
    openModal();
    }

    function onEdit(e) {
    const id = e.currentTarget.dataset.id;
    prefillFromCard(id);
    const title = qs('#modal-product .modal-title');
    if (title) title.textContent = 'Edit Product';    // ← judul
    openModal();
    }

  function onDelete(e) {
    pendingDeleteId = e.currentTarget.dataset.id;
    openDel();
  }

  // Submit create/update
  async function onSubmitForm(e) {
    e.preventDefault();
    try {
      const idVal = (fId && fId.value) ? String(fId.value) : "";
      const isEdit = Boolean(idVal);
      const url = isEdit ? buildUpdateUrl(idVal) : EP.create;

      // Kirim sebagai FormData (mendukung file jika nanti kamu tambahkan)
      const fd = new FormData(form);
      // Jika edit, pastikan ID tidak terkirim sebagai field yang mengganggu, aman saja dibiarkan.

      const res = await fetchJSON(url, { method: "POST", data: fd });
      showToast(isEdit ? "Produk diperbarui" : "Produk dibuat", "info");
      closeModal();
      await loadList();
    } catch (err) {
      console.error(err);
      showToast(simplifyErrors(err.payload?.errors) || err.message || "Gagal menyimpan", "error");
    }
  }

  // Konfirmasi delete
  async function onConfirmDelete() {
    if (!pendingDeleteId) return closeDel();
    try {
      const url = buildDeleteUrl(pendingDeleteId);
      await fetchJSON(url, { method: "POST" }); // sesuai view: POST/DELETE
      showToast("Produk dihapus", "info");
      closeDel();
      await loadList();
    } catch (err) {
      console.error(err);
      showToast("Gagal menghapus", "error");
    }
  }

  // ----- BIND EVENTS -----
  btnRefresh && btnRefresh.addEventListener("click", loadList);
  btnOpenCreate && btnOpenCreate.addEventListener("click", onCreate);
  btnOpenCreate2 && btnOpenCreate2.addEventListener("click", onCreate);
  btnCancel && btnCancel.addEventListener("click", closeModal);

  btnDelCancel && btnDelCancel.addEventListener("click", closeDel);
  btnDelYes && btnDelYes.addEventListener("click", onConfirmDelete);

  form && form.addEventListener("submit", onSubmitForm);

  // Tutup saat klik backdrop & tombol X
    btnX && btnX.addEventListener("click", closeModal);
    btnDelX && btnDelX.addEventListener("click", closeDel);

    document.addEventListener("click", (e) => {
    // backdrop ada di dalam #modal-product / #modal-delete
    if (e.target?.classList?.contains("backdrop")) {
        const parentId = e.target.parentElement?.id;
        if (parentId === "modal-product") closeModal();
        if (parentId === "modal-delete") closeDel();
    }
    });


  // ----- INIT -----
  // Muat list saat halaman siap
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", loadList);
  } else {
    loadList();
  }

  // ----- Util: escape HTML -----
  function escapeHtml(str) {
    return String(str || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }
})();
