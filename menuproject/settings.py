import os
from dotenv import load_dotenv
from pathlib import Path
import logging
import dj_database_url
from decouple import config
from corsheaders.defaults import default_headers

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

ATONNA_APP_TOKEN = os.environ.get("DJANGO_ATONNA_APP_TOKEN")
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
APP_NAME = os.environ.get("DJANGO_APP_NAME")

DEBUG = os.environ.get("DJANGO_ENV", "development").lower() != "production"

# CSRF_TRUSTED_ORIGINS = ['https://atonna-backend-462b5d0ade20.herokuapp.com']
   
CORS_ORIGIN_ALLOW_ALL = False  # Keep it secure

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "atonna-backend-a6bdca67b05e.herokuapp.com",
    "snmenusidekick.com",
    "snmenu.com",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://snmenusidekick.com",
    "https://www.snmenusidekick.com",
    "https://snmenu.com",
    "https://www.snmenu.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://snmenusidekick.com",
    "https://www.snmenusidekick.com",  # Add 'www' version
    "https://snmenu.com",
    "https://www.snmenu.com",  # Add 'www' version
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    *default_headers,
    "ATONNA-APP-TOKEN",
)

# DJANGO_SETTINGS_MODULE = 'menuproject.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "menuproject.settings")

CLOUDINARY_LOGO_URL = "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1741277593/DigitalMenuLogo_n5m7y5.jpg"

ROOT_URLCONF = 'menuproject.urls'

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "menuproject.api",  
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Add your templates directory if needed
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

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# MIDDLEWARE.append('menuproject.settings.LogHostMiddleware')  # Add this line

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# DATABASES = {
#     'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
# }

# Detect if running on Heroku
ON_HEROKU = False

if ON_HEROKU:
    DATABASES = {
        'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv("LOCAL_DB_NAME", "your_local_db_name"),
            'USER': os.getenv("LOCAL_DB_USER", "your_local_db_user"),
            'PASSWORD': os.getenv("LOCAL_DB_PASSWORD", "your_local_db_password"),
            'HOST': os.getenv("LOCAL_DB_HOST", "localhost"),
            'PORT': os.getenv("LOCAL_DB_PORT", "5432"),
        }
    }

TIME_ZONE = "America/Santiago"
USE_TZ = True

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

WEBPAY_API_KEY = os.environ.get("WEBPAY_API_KEY")
WEBPAY_COMMERCE_CODE = os.environ.get("WEBPAY_COMMERCE_CODE")
WEBPAY_INTEGRATION_TYPE = os.environ.get("WEBPAY_INTEGRATION_TYPE")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DJANGO_ENV = os.environ.get("DJANGO_ENV", "development").lower()

if DJANGO_ENV == "production":
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    
SECURE_SSL_REDIRECT = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
