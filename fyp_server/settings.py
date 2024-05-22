"""
Django settings for fyp_server project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-y0s2qlz&02=7x#6e^)j3_wt3knml8s^cs+&nr!-u0wggn_)%&')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notifications.apps.NotificationsConfig',
    'api.apps.ApiConfig',
    'dashboard.apps.DashboardConfig',
    
    'corsheaders',
    'rest_framework',
    'channels',
    'celery',
    # 'webpush',
    # 'pandas',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fyp_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'fyp_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if RENDER_EXTERNAL_HOSTNAME:
    DATABASES['default'] = dj_database_url.config(
            default=os.environ.get("DATABASE_URL"),
            conn_max_age=600
        )
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Channels
ASGI_APPLICATION = "fyp_server.asgi.application"
CHANNEL_LAYERS = {
    # 'default': {
    #     'BACKEND': 'channels.layers.InMemoryChannelLayer',
    # },
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)]
        }
    }
}

#CELERY config
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

if not DEBUG:
    CELERY_BROKER_URL = os.environ.get('REDIS_URL')
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')
    CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [(os.environ.get('REDIS_URL'))]

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'Check_For_Offline_Transformers': {
        'task': 'api.tasks.check_off_transformers',
        'schedule': crontab(minute="*/15"),
    },
    'Check_For_Overloaded_Transformers': {
        'task': 'api.tasks.check_overloaded_transformers',
        'schedule': crontab(hour="*/1", minute=0),
    },
}


# LOGIN_URL='/dashboard/login'
# LOGIN_REDIRECT_URL = '/dashboard'
# LOGOUT_REDIRECT_URL = LOGIN_URL


CSRF_TRUSTED_ORIGINS = ['http://localhost:3001', 'https://fyp-server-django.onrender.com']
# CSRF_COOKIE_DOMAIN = 'http://localhost:8000'

# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',
#     # Add other allowed origins if needed
# ]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3001',
    'https://transformer-web-dashboard.onrender.com',
]

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True



# WEBPUSH_SETTINGS = {
#     "VAPID_PUBLIC_KEY": "BAfqkyI1TUgXVAtPQ8rJ3VMvpojxnubiGhl2PuFS7FzW-BBamtNNVdSaM1m5bLP_qsKKubroThFxFEBKvldGyEM",
#     "VAPID_PRIVATE_KEY": "nro5cMMgO4bba-s4opOdlJkCp_OZ2kpSkYczlaECcsQ",
#     "VAPID_ADMIN_EMAIL": "kldenis2001@gmail.com",
# }
