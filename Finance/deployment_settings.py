import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from .settings import *  # Import base settings

# -----------------------------
# Debug & Secret Key
# -----------------------------
DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY)
if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY environment variable is required.")

# -----------------------------
# Allowed Hosts / CSRF / Session
# -----------------------------
RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
BACKEND_DOMAIN = RENDER_HOSTNAME or "localhost"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
if BACKEND_DOMAIN:
    ALLOWED_HOSTS.append(BACKEND_DOMAIN)

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = []
if BACKEND_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f"https://{BACKEND_DOMAIN}")
    CSRF_TRUSTED_ORIGINS.append(f"http://{BACKEND_DOMAIN}")

# Ensure secure cookies
SESSION_COOKIE_SECURE = True   # Works only on HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SECURE_SSL_REDIRECT = True     # Redirect HTTP -> HTTPS

# -----------------------------
# CORS (Frontend URL)
# -----------------------------
FRONTEND_URL = os.environ.get(
    "FRONTEND_URL",
    "https://finotreasuryx.onrender.com"
)

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
    FRONTEND_URL.replace("https://", "http://")
]

# -----------------------------
# Static & Media Files (WhiteNoise)
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
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
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

# -----------------------------
# Optional: Security headers
# -----------------------------
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
