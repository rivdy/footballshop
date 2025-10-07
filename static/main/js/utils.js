// ====================== utils.js ======================
// Helper umum: CSRF, Fetch JSON, Toast, DOM, Format, Form

// --- Cookie & CSRF ---
function getCookie(name) {
  const cookies = document.cookie ? document.cookie.split(";") : [];
  for (let c of cookies) {
    c = c.trim();
    if (c.startsWith(name + "=")) return decodeURIComponent(c.substring(name.length + 1));
  }
  return "";
}

function getCSRFToken() {
  // 1) coba dari cookie csrftoken (standar Django)
  const fromCookie = getCookie("csrftoken");
  if (fromCookie) return fromCookie;
  // 2) fallback dari meta (pastikan <meta name="csrf-token" content="{{ csrf_token }}"> di base.html)
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) return meta.getAttribute("content") || "";
  // 3) fallback dari input hidden (mis. dalam form)
  const input = document.querySelector('input[name="csrfmiddlewaretoken"]');
  if (input) return input.value || "";
  return "";
}

// --- Fetch JSON (x-www-form-urlencoded by default) ---
async function fetchJSON(url, { method = "GET", data = null, headers = {}, signal } = {}) {
  const opts = { method, headers: { "X-Requested-With": "XMLHttpRequest", ...headers }, signal };

  // Tambahkan CSRF untuk metode tulis
  const needsCSRF = !["GET", "HEAD", "OPTIONS", "TRACE"].includes(method.toUpperCase());
  if (needsCSRF) {
    const csrf = getCSRFToken();
    if (csrf) opts.headers["X-CSRFToken"] = csrf;
  }

  if (data) {
    if (data instanceof FormData) {
      // biarkan browser set Content-Type dengan boundary
      opts.body = data;
    } else if (data instanceof URLSearchParams) {
      opts.headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8";
      opts.body = data.toString();
    } else if (typeof data === "object") {
      // encode sebagai x-www-form-urlencoded (sesuai petunjuk tutorial)
      const params = new URLSearchParams();
      for (const [k, v] of Object.entries(data)) params.append(k, v ?? "");
      opts.headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8";
      opts.body = params.toString();
    } else {
      // string mentah (mis. sudah di-encode)
      opts.body = data;
    }
  }

  const res = await fetch(url, opts);
  // upayakan parse JSON; jika gagal, buat objek minimal
  let json = {};
  try { json = await res.json(); } catch (_) { json = {}; }

  if (!res.ok || json.ok === false) {
    const msg =
      json.error ||
      (json.errors ? simplifyErrors(json.errors) : `HTTP ${res.status} ${res.statusText}`);
    const err = new Error(msg);
    err.status = res.status;
    err.payload = json;
    throw err;
  }
  return json;
}

// --- Errors helper: ubah object errors -> string ringkas ---
function simplifyErrors(errs) {
  try {
    if (typeof errs === "string") return errs;
    if (Array.isArray(errs)) return errs.join(", ");
    if (typeof errs === "object" && errs !== null) {
      // contoh: {name: ["This field is required."], price: ["Enter a number."]}
      const parts = [];
      for (const [k, v] of Object.entries(errs)) {
        const val = Array.isArray(v) ? v.join(" ") : String(v);
        parts.push(`${k}: ${val}`);
      }
      return parts.join(" | ");
    }
  } catch (_) {}
  return "Terjadi kesalahan.";
}

// --- Toast sederhana ---
function ensureToastContainer() {
  let wrap = document.getElementById("toast");
  if (!wrap) {
    wrap = document.createElement("div");
    wrap.id = "toast";
    wrap.style.position = "fixed";
    wrap.style.right = "16px";
    wrap.style.bottom = "16px";
    wrap.style.zIndex = "50";
    document.body.appendChild(wrap);
  }
  return wrap;
}

function showToast(text, kind = "info", timeout = 2500) {
  const wrap = ensureToastContainer();
  const el = document.createElement("div");
  el.style.marginTop = "8px";
  el.style.border = "1px solid var(--stroke)";
  el.style.borderRadius = "12px";
  el.style.padding = "10px 14px";
  el.style.background = "#121218";
  el.style.boxShadow = "var(--shadow)";
  el.style.color = kind === "error" ? "#fecaca" : "#fff";
  el.textContent = text;
  wrap.appendChild(el);
  window.setTimeout(() => el.remove(), timeout);
}

// --- DOM helpers ---
function qs(sel, parent = document) { return parent.querySelector(sel); }
function qsa(sel, parent = document) { return Array.from(parent.querySelectorAll(sel)); }
function show(el) { if (el) el.style.display = ""; }
function hide(el) { if (el) el.style.display = "none"; }
function toggle(el, force) {
  if (!el) return;
  if (typeof force === "boolean") { el.style.display = force ? "" : "none"; return; }
  el.style.display = (el.style.display === "none" || getComputedStyle(el).display === "none") ? "" : "none";
}

// --- Format helper ---
function formatIDR(num) {
  const n = Number(num || 0);
  return new Intl.NumberFormat("id-ID", { maximumFractionDigits: 0 }).format(n);
}

// --- Form helpers ---
function formToFormData(form) {
  // Konversi <form> DOM ke FormData
  return new FormData(form);
}

function formToParams(form) {
  // Jika ingin x-www-form-urlencoded dari form
  const fd = new FormData(form);
  const params = new URLSearchParams();
  for (const [k, v] of fd.entries()) params.append(k, v);
  return params;
}

// --- Endpoint helper: ganti ID pada pola URL seperti /ajax/products/0/update/ -> /ajax/products/123/update/ ---
function buildUrlWithId(patternUrl, id) {
  // asumsi pattern memakai angka 0 sebagai placeholder
  return patternUrl.replace(/\/0(\/|$)/, `/${id}$1`);
}

// Expose ke global (opsional)
window.utils = {
  getCSRFToken,
  fetchJSON,
  showToast,
  qs, qsa, show, hide, toggle,
  formatIDR,
  formToFormData,
  formToParams,
  buildUrlWithId,
};
