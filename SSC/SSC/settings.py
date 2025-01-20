import os
from pathlib import Path
from .encrypt_decrypt import base64_to_text
import logging
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

logs_dir = os.path.join(BASE_DIR, 'logs')
os.makedirs(logs_dir, exist_ok=True)


class ExcludeURLResolverLogs(logging.Filter):
    def filter(self, record):
        return 'URLResolver' not in record.getMessage()


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'filters': {
        'exclude_url_resolver': {
            '()': ExcludeURLResolverLogs,
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(logs_dir, 'application.log'),
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'filters': ['exclude_url_resolver'],  # Apply the filter
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.utils.autoreload': {  # Suppress autoreload debug logs
            'handlers': ['console'],  # Reference the console handler
            'level': 'WARNING',  # Ignore DEBUG messages
            'propagate': False,
        },
        'ClientDetail': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'Property': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'SorterSession': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^8cv(#$rb2-v%ug(4sls*gec&ym58ub66^g_72siu6c9&9%vwk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'ClientDetail',
    'Property',
    'SorterSession',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SSC.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

WSGI_APPLICATION = 'SSC.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'static'),
]

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR,'media')


# AWS S3 Configuration
AWS_ACCESS_KEY_ID = base64_to_text('QUtJQVQ3SkpVMkpCQkNMTVA0Tko=')
AWS_SECRET_ACCESS_KEY = base64_to_text('ZnE4SHdESHZxdkVWUEMwbHI0TUxWYlgzRDQxbjBZV1hXeUxuMlBGbA==')
AWS_STORAGE_BUCKET_NAME = 'ssc-disrupt'
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_QUERYSTRING_AUTH = False


# S3 Media Files Configuration
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'

# Cache Control (Optional, for performance)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
