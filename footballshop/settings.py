"""
Django settings for footballshop project.
"""

import os
from pathlib import Path

# === BASE & MODE ===
BASE_DIR = Path(__file__).resolve().parent.parent

PRODUCTION = os.getenv("PRODUCTION", "False").lower() == "true"
DEBUG = not PRODUCTION

# === HOSTS & CSRF ===
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "10.0.2.2",  # emulator Android
    
    "rivaldy-putra-footballshop.pbp.cs.ui.ac.id",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    "https://rivaldy-putra-footballshop.pbp.cs.ui.ac.id",
]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-2g6w+er$29hr!y6k699x-oka+n$92ffkvg*^(e%n9i+s^nwy_7"

# === APPS ===
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "corsheaders",          # untuk CORS
    "main",
    "authentication",       # nanti dipakai untuk login/register API
]

# === MIDDLEWARE ===
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS harus di atas SessionMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "footballshop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": ["django.contrib.humanize.templatetags.humanize"],
        },
    },
]

WSGI_APPLICATION = "footballshop.wsgi.application"

# === DATABASE ===
SQLITE = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

if os.getenv("DJANGO_DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DJANGO_DB_NAME"),
            "USER": os.getenv("DJANGO_DB_USER"),
            "PASSWORD": os.getenv("DJANGO_DB_PASSWORD"),
            "HOST": os.getenv("DJANGO_DB_HOST"),
            "PORT": os.getenv("DJANGO_DB_PORT", "5432"),
            "OPTIONS": {"options": "-c search_path=public"},
        }
    }
else:
    DATABASES = SQLITE

# === PASSWORD VALIDATION ===
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# === I18N ===
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# === STATIC FILES ===
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# === CORS & COOKIE SETTINGS UNTUK FLUTTER ===
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CSRF_COOKIE_SECURE = PRODUCTION
SESSION_COOKIE_SECURE = PRODUCTION

CSRF_COOKIE_SAMESITE = 'None' if PRODUCTION else 'Lax'
SESSION_COOKIE_SAMESITE = 'None' if PRODUCTION else 'Lax'
LOGIN_URL = '/auth/login/'