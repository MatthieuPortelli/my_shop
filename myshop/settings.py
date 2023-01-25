from pathlib import Path
from django.contrib import messages
from decouple import config
import environ
import os

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIRS = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'portellim.pythonanywhere.com',
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'account',
    'mathfilters',
    'django_extensions',
    'captcha',
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

ROOT_URLCONF = 'myshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIRS],
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

WSGI_APPLICATION = 'myshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MAIL CONFIRMATION SETTINGS
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = env('EMAIL_HOST')
# EMAIL_FROM = env('EMAIL_FROM')
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = env('EMAIL_PORT')
# EMAIL_USE_TLS = env('EMAIL_USE_TLS')
# PASSWORD_RESET_TIMEOUT = env('PASSWORD_RESET_TIMEOUT')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Utilisation de GMAIL
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'mywebsite.python@gmail.com'
EMAIL_HOST_USER = 'mywebsite.python@gmail.com'
EMAIL_HOST_PASSWORD = 'jzimuimwmqhfcxhq'
EMAIL_PORT = 587
# Indique si une connexion TLS (sécurisée) doit être utilisée pour le dialogue avec le serveur SMTP
EMAIL_USE_TLS = True
# Délai avant expiration du token
PASSWORD_RESET_TIMEOUT = 14400

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# CAPTCHA
# RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
# RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PUBLIC_KEY')

RECAPTCHA_PUBLIC_KEY = '6LffdyckAAAAACH9sqvPOM0UKwj7fMlWeXXwEr2b'
RECAPTCHA_PRIVATE_KEY = '6LffdyckAAAAANO2s0YdAd_0dblXW8Njv_Ah5sTM'

GOOGLE_RECAPTCHA_SECRET_KEY = '6LffdyckAAAAANO2s0YdAd_0dblXW8Njv_Ah5sTM'
