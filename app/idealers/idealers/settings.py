import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = int(os.getenv('DEBUG', default=0))

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'authentication.Dealer'

APPROVED_ALLOWED_DEALERS = eval(os.getenv('APPROVED_ALLOWED_DEALERS', '[]'))

EXTERNAL_CASHBACK_API = os.getenv('EXTERNAL_CASHBACK_API')
EXTERNAL_CASHBACK_API_TOKEN = os.getenv('EXTERNAL_CASHBACK_API_TOKEN')
EXTERNAL_CASHBACK_API_TOKEN_HEADER = os.getenv('EXTERNAL_CASHBACK_API_TOKEN_HEADER')

# Cashback Rules
FIRST_LEVEL_CASHBACK_TARGET = int(os.getenv('FIRST_LEVEL_CASHBACK_TARGET', '1000'))
FIRST_LEVEL_CASHBACK_PERCENT = os.getenv('FIRST_LEVEL_CASHBACK_PERCENT', '0.1')

SECOND_LEVEL_CASHBACK_TARGET = int(os.getenv('SECOND_LEVEL_CASHBACK_TARGET', '1500'))
SECOND_LEVEL_CASHBACK_PERCENT = os.getenv('SECOND_LEVEL_CASHBACK_PERCENT', '0.15')

THIRD_LEVEL_CASHBACK_PERCENT = os.getenv('THIRD_LEVEL_CASHBACK_PERCENT', '0.2')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework_simplejwt',

    ## Project apps
    'api',
    'authentication',
    'cashback',
    'orders',
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

ROOT_URLCONF = 'idealers.urls'

WSGI_APPLICATION = 'idealers.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('POSTGRES_DB', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.getenv('POSTGRES_USER', 'user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'password'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
