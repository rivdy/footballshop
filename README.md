# Garuda Football Shop

**PWS:** https://rivaldy-putra-footballshop.pbp.cs.ui.ac.id/

## 1) Implementasi checklist (step-by-step)
1. **Proyek Django baru**  
   Membuat folder `footballshop`, membuat virtualenv, menulis `requirements.txt`, lalu `django-admin startproject footballshop .`.
2. **Membuat aplikasi `main`**  
   `python manage.py startapp main`, mendaftarkan `'main'` ke `INSTALLED_APPS`.
3. **Routing proyek → app**  
   Di `footballshop/urls.py` menambahkan `path('', include('main.urls'))`. Di `main/urls.py` memetakan root ke view `show_home`.
4. **Model `Product`**  
   Menambahkan model dengan 6 atribut wajib (`name`, `price`, `description`, `thumbnail`, `category`, `is_featured`) + atribut opsional (mis. `stock`, `brand`, `rating`). Lalu `makemigrations` dan `migrate`.
5. **View + Template**  
   Membuat fungsi `show_home` di `main/views.py` yang mengirim `context` berisi `app_name`, `student_name`, dan `student_class` ke `main/templates/home.html`. Template menampilkan tiga data tersebut.
6. **Deployment**  
   Menambahkan domain PWS ke `ALLOWED_HOSTS`, mengisi Environs `.env.prod` (PRODUCTION=True, SCHEMA=tugas_individu, DB_*), lalu `git push pws master`.
7. **README**  
   Menulis penjelasan langkah, bagan alur MVT, peran `settings.py`, migrasi, alasan memakai Django, dan feedback asdos.

## 2) Bagan request–response & kaitan berkas (MVT)
