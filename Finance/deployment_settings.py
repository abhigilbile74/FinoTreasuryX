import os 
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from .settings import *
from .settings import BASE_DIR

RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
if RENDER_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_HOSTNAME]
    CSRF_TRUSTED_ORIGINS = [f'https://{RENDER_HOSTNAME}']
else:
    ALLOWED_HOSTS = []
    CSRF_TRUSTED_ORIGINS = []

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY)

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # add this line
    'django.middleware.common.CommonMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",  # Vite
#     "http://localhost:3000",  # CRA
# ]

STORAGES = {
    "default":{
        "BACKEND":"django.core.files.storage.FileSystemStorage",
    },
    "staticfiles":{
        "BACKEND":"whitenoise.storage.CompressedManifestStaticFilesStorage",
    },

}

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ImproperlyConfigured("DATABASE_URL environment variable is required.")

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=int(os.environ.get("DB_CONN_MAX_AGE", "600")),
    )
}