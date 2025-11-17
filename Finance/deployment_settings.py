import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from .settings import *   # ← IMPORT EVERYTHING, NOT ONLY BASE_DIR

# -----------------------------
# ALLOWED_HOSTS / CSRF / CORS
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

# CORS Configuration for Production
# Get frontend URL from environment or default to empty list
FRONTEND_URL = os.environ.get("FRONTEND_URL", "")
if FRONTEND_URL:
    CORS_ALLOWED_ORIGINS = [FRONTEND_URL]
    CORS_ALLOW_ALL_ORIGINS = False
else:
    # If no frontend URL specified, disable CORS_ALLOW_ALL_ORIGINS
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = []

# -----------------------------
# Static files (WhiteNoise)
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Add WhiteNoise middleware after SecurityMiddleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Add WhiteNoise middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # Use CompressedStaticFilesStorage instead of CompressedManifestStaticFilesStorage
        # to avoid 502 errors if manifest.json is missing or incomplete
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# -----------------------------
# Logging Configuration
# -----------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'whitenoise': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
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
        conn_health_checks=True,  # Enable connection health checks
    )
}
