import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from .settings import *   # ← IMPORT EVERYTHING, NOT ONLY BASE_DIR

# -----------------------------
# ALLOWED_HOSTS / CSRF
# -----------------------------
RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

if RENDER_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_HOSTNAME)
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_HOSTNAME}"]
else:
    CSRF_TRUSTED_ORIGINS = []

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY)

# -----------------------------
# Static files (WhiteNoise)
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# -----------------------------
# Database
# -----------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ImproperlyConfigured("DATABASE_URL environment variable is required.")

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=int(os.environ.get("DB_CONN_MAX_AGE", "600")),
    )
}
