import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from .settings import *   # Import base settings


# -----------------------------
# Debug & Secret Key
# -----------------------------
DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY)


# -----------------------------
# Allowed Hosts / CSRF
# -----------------------------
RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

if RENDER_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_HOSTNAME)

CSRF_TRUSTED_ORIGINS = [
    f"https://{RENDER_HOSTNAME}"
] if RENDER_HOSTNAME else []


# -----------------------------
# CORS (Frontend URL)
# -----------------------------
FRONTEND_URL = os.environ.get(
    "FRONTEND_URL",
    "https://frontendfinotreasuryx.onrender.com"
)

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [FRONTEND_URL]


# -----------------------------
# Static Files (WhiteNoise)
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# -----------------------------
# Database (PostgreSQL - Render)
# -----------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ImproperlyConfigured("DATABASE_URL environment variable is required.")

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# -----------------------------
# Logging
# -----------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
