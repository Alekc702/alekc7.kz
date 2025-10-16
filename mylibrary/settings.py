import os
from pathlib import Path

# Optional: use dj_database_url in production (installed from requirements on Render)
try:
    import dj_database_url  # type: ignore
except Exception:  # package may be missing in a local venv
    dj_database_url = None

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'change-me-for-production')

# Default to True for development unless DJANGO_DEBUG is explicitly set to 'False'
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# By default allow localhost and loopback addresses for development.
# For production set DJANGO_ALLOWED_HOSTS environment variable to a comma-separated list.
# Also append RENDER_EXTERNAL_HOSTNAME automatically if present.
def _csv_env(name: str, default: str = "") -> list[str]:
    raw = os.environ.get(name, default)
    return [item.strip() for item in raw.split(',') if item.strip()]

ALLOWED_HOSTS = _csv_env('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1')

# Include Render-provided hostname (e.g., <service>.onrender.com) to prevent DisallowedHost 400s
_render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if _render_host and _render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_render_host)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'games.apps.GamesConfig',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'mylibrary.middleware.ApiKeyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mylibrary.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mylibrary.wsgi.application'

# Database
# If DATABASE_URL is set and dj_database_url is available, use it; otherwise fallback to sqlite3
if os.environ.get('DATABASE_URL') and dj_database_url is not None:
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ['DATABASE_URL'],
            conn_max_age=600,
            ssl_require=not (os.environ.get('DJANGO_DEBUG', 'True') == 'True')
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
# On Render: if DJANGO_USE_S3=True, use S3. Otherwise, honor DJANGO_MEDIA_ROOT if provided (e.g., /var/data/media),
# falling back to a local folder for development.
MEDIA_ROOT = Path(os.environ.get('DJANGO_MEDIA_ROOT', BASE_DIR / 'media'))

# Make sure MEDIA_ROOT exists at startup (harmless if already exists)
try:
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)  # type: ignore[attr-defined]
except Exception:
    pass

# Optional S3-compatible storage (Cloudflare R2, AWS S3, etc.)
USE_S3 = os.environ.get('DJANGO_USE_S3', 'False') == 'True'
if USE_S3:
    # Minimal config: bucket and credentials
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')  # e.g., https://<accountid>.r2.cloudflarestorage.com
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', '')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    # Storage settings
    INSTALLED_APPS.append('storages')
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_DEFAULT_ACL = None
    AWS_S3_OBJECT_PARAMETERS = { 'CacheControl': 'max-age=86400' }
    # Media URL becomes the S3 endpoint + bucket
    if AWS_S3_ENDPOINT_URL and AWS_STORAGE_BUCKET_NAME:
        MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# WhiteNoise settings
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# API key for simple token-based access to JSON endpoints
# Set DJANGO_API_KEY in the environment to enable access; requests must send this
# value either as the 'X-API-Key' header or as the 'api_key' query parameter.
API_KEY = os.environ.get('DJANGO_API_KEY', '').strip()

# Security & proxy headers (Render/Nginx)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 0 if DEBUG else 60 * 60 * 24 * 7  # 1 week
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

# CSRF trusted origins (needed for HTTPS on custom domains and Render)
_csrf_from_env = os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS')
if _csrf_from_env:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_from_env.split(',') if o.strip()]
else:
    # By default trust Render subdomains; add your custom domain via env in production
    CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']
 
