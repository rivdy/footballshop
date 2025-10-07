// ====================== auth.js ======================
(function () {
  // --- Ambil endpoints dari #endpoints (kalau ada), kalau tidak pakai default ---
  const epEl = document.getElementById("endpoints");
  const EP = {
    login:   epEl?.dataset.login   || "/ajax/login/",
    register:epEl?.dataset.register|| "/ajax/register/",
    logout:  epEl?.dataset.logout  || "/ajax/logout/",
  };

  // --- Helper redirect kecil ---
  function go(url) { window.location.href = url; }

  // ========== LOGIN ==========
  // Harapkan form login punya id="login-form"
  const loginForm = document.getElementById("login-form") || document.querySelector('form[data-auth="login"]');
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      try {
        const data = formToParams(loginForm); // x-www-form-urlencoded
        const res = await fetchJSON(EP.login, { method: "POST", data });
        showToast("Login berhasil", "info");
        // Redirect: ambil dari data-redirect jika disediakan, kalau tidak ke halaman list
        const to = loginForm.dataset.redirect || "/";
        go(to);
      } catch (err) {
        showToast(err.message || "Login gagal", "error");
      }
    });
  }

  // ========== REGISTER ==========
  // Harapkan form register punya id="register-form"
  const registerForm = document.getElementById("register-form") || document.querySelector('form[data-auth="register"]');
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      try {
        const data = formToParams(registerForm);
        const res = await fetchJSON(EP.register, { method: "POST", data });
        showToast("Registrasi berhasil. Silakan login.", "info");
        // Setelah register, arahkan ke halaman login (bisa override via data-redirect)
        const to = registerForm.dataset.redirect || "/login/";
        go(to);
      } catch (err) {
        showToast(simplifyErrors(err.payload?.errors) || err.message || "Registrasi gagal", "error");
      }
    });
  }

  // ========== LOGOUT ==========
  // Bisa berupa <form id="logout-form"> atau tombol <button data-action="logout">
  const logoutForm = document.getElementById("logout-form") || document.querySelector('form[data-auth="logout"]');
  if (logoutForm) {
    logoutForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      try {
        await fetchJSON(EP.logout, { method: "POST" });
        showToast("Logout berhasil", "info");
        const to = logoutForm.dataset.redirect || "/login/";
        go(to);
      } catch (err) {
        showToast("Logout gagal", "error");
      }
    });
  }

  const logoutBtns = document.querySelectorAll('[data-action="logout"]');
  logoutBtns.forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      try {
        await fetchJSON(EP.logout, { method: "POST" });
        showToast("Logout berhasil", "info");
        const to = btn.dataset.redirect || "/login/";
        go(to);
      } catch (err) {
        showToast("Logout gagal", "error");
      }
    });
  });

  // Catatan:
  // - Pastikan di halaman login/register ada baris:
  //   <script src="{% static 'main/js/utils.js' %}"></script>
  //   <script src="{% static 'main/js/auth.js' %}"></script>
  // - Di base.html sudah ditambahkan:
  //   <meta name="csrf-token" content="{{ csrf_token }}">
  // - Kalau mau override redirect:
  //   <form id="login-form" data-redirect="{% url 'main:show_products' %}">...</form>
})();
