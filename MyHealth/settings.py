"""
Django settings for MyHealth project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wylyio30rd*)k1)h1pn0w@g-uz@roou3to15%^w(j7)&j$c686'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['myhealth-dev.ap-southeast-1.elasticbeanstalk.com', '127.0.0.1','myhealth2-dev.ap-southeast-1.elasticbeanstalk.com','172.31.22.137']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'general',
    'patient',
    'doctor',
    'clinicadmin',
    'systemadmin',
    'storages',
    #'django_q',
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

ROOT_URLCONF = 'MyHealth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
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

WSGI_APPLICATION = 'MyHealth.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True


env = environ.Env()
environ.Env.read_env()

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.BaseUser'

LOGIN_REDIRECT_URL = 'redirect'
LOGOUT_REDIRECT_URL = 'home'

STATIC_URL = 'static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

### Django storages - use this for production
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

### Django storages - use in production
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

#EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
#EMAIL_FILE_PATH = str(BASE_DIR.joinpath('sent_emails'))

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#DEFAULT_FROM_EMAIL = 'test@test.com'
if 'EMAIL_HOST' in os.environ:
  DEFAULT_FROM_EMAIL = os.environ['EMAIL_HOST_USER']
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = os.environ['EMAIL_HOST']
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True
  EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
  EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
else:
  DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = env('EMAIL_HOST')
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True
  EMAIL_HOST_USER = env('EMAIL_HOST_USER')
  EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

#Q_CLUSTER = {
#    "name": "createslots",
#    "orm": "default",  # Use Django's ORM + database for broker
#}

if 'AWS_ACCESS_KEY_ID' in os.environ:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']