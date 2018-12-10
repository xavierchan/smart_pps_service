"""
Django settings for smart_pps_service project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import datetime
from env import *
import djcelery
djcelery.setup_loader()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5kuo*-vgs-jp3-zmbmnfl160=-g*4xh@n7mjr0r47&5^-m$lu9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
APPEND_SLASH = False

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'raven.contrib.django.raven_compat',
    'djcelery',
    'social_django',
    'notifications',
    'actstream',
    #'channels',
    # 'account',
    'analytical',
    #'robots',
    'mdeditor',
]

LOCAL_APPS = [
    'member',
    'pps',
    'finance',
    'aliyun_oss',
    'blog',
    'crawler',
    'game',
    'comic',
    'music',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS;


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'PAGE_SIZE': 10,
    'NON_FIELD_ERRORS_KEY': 'error',

    'DEFAULT_THROTTLE_RATES': {
        'captcha_min': '1/min',
        'captcha_hour': '5/hour',
    },

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}
LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

JWT_AUTH = {
    # 'JWT_PAYLOAD_HANDLER':
    # 'elite_live_restapi.jwt_handler.jwt_payload_handler',

    # 'JWT_RESPONSE_PAYLOAD_HANDLER':
    # 'elite_live_restapi.jwt_handler.jwt_response_payload_handler',

    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_ALLOW_REFRESH': True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE_CLASSES = [
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
]


AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.yahoo.YahooOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.weixin.WeixinOAuth2',
    'social_core.backends.weibo.WeiboOAuth2',
    'social_core.backends.qq.QQOAuth2',
    'social_core.backends.douban.DoubanOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'smart_pps_service.urls'

SWAGGER_SETTINGS = {
    'SHOW_REQUEST_HEADERS': True,
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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'smart_pps_service.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if False:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            "ENGINE": "django.db.backends.mysql",
            "HOST": MYSQL.get('HOST'),
            "PORT": MYSQL.get('PORT'),
            "NAME": MYSQL.get('NAME'),
            "USER": MYSQL.get('USER'),
            "PASSWORD": MYSQL.get('PASSWORD'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': 'SET default_storage_engine=INNODB',
            },
            'TEST_CHARSET': 'utf8',
            'TEST_COLLATION': 'utf8_general_ci'
        },
    }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_URL = '/login'

SITE_ID = 1

FMT_DATETIME = "%Y-%m-%d %H:%M:%S"
FMT_DATE = "%Y-%m-%d"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)


CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

TEMPLATE_CONTEXT_PROCESSORS = [
    "account.context_processors.account",
]

SOCIAL_AUTH_GITHUB_KEY = 'dc0df6a5de9d855a7cdd'
SOCIAL_AUTH_GITHUB_SECRET = 'f6d66b3d1b51c097cc4d4c862faeac7ec9fa1880'
