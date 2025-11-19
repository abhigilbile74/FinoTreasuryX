import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from .settings import *

# ----------------------------------------
# Debug & Secret Key
# ----------------------------------------
DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY)
if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY environment variable is required.")

# ----------------------------------------
# Allowed Hosts / Backend Domain
# ----------------------------------------
RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")  # provided by Render
BACKEND_DOMAIN = RENDER_HOSTNAME or "finotreasuryx-1.onrender.com"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    BACKEND_DOMAIN,
]

# ----------------------------------------
# CSRF Trusted Origins
# ----------------------------------------
CSRF_TRUSTED_ORIGINS = [
    "https://finotreasuryx-1.onrender.com",
    "https://frontendfinotreasuryx.onrender.com",
]

# ----------------------------------------
# CORS Settings
# ----------------------------------------
FRONTEND_URL = os.environ.get(
    "FRONTEND_URL",
    "https://frontendfinotreasuryx.onrender.com"
)

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
]

# Allow all Render subdomains (optional but helpful)
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.onrender\.com$",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "accept",
    "origin",
    "user-agent",
    "accept-encoding",
    "x-csrftoken",
    "x-requested-with",
]

# ----------------------------------------
# Static & Media
# ----------------------------------------
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

# ----------------------------------------
# Database (PostgreSQL)
# ----------------------------------------
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

# ----------------------------------------
# Logging
# ----------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}

# ----------------------------------------
# Security Settings
# ----------------------------------------
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # MUST remain False for frontend JS to send CSRF

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
