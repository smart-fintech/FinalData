"""
Django settings for e_checkproject project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=^dz+bda_coz4b13m27a@l2p0(k*b5u_gm22cpy-7k30y0zupe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','0.0.0.0']

AUTH_USER_MODEL='accountapp.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    # 'e_checkapp',
    # 'posts',
    'corsheaders',
    # 'paidmodule.apps.PaidmoduleConfig',
    'tallyapp',
    'otheruser',
    'invoice',         
    'e_payment',
    'accountapp',
    # 'pymentroll',
    # 'sorl.thumbnail'
   
    
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',    #cross sitemiddleware
    'django.middleware.common.BrokenLinkEmailsMiddleware', #cross sitemiddlwware
    'django.middleware.common.CommonMiddleware',# crosssite middleware

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(os.path.join(BASE_DIR, 'templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'tallyapp.context_processors.get_ledeger_auto',
                # 'tallyapp.context_processors.get_company_name_auto'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

CORS_ORIGIN_ALLOW_ALL=True
ALLOWED_HOSTS=['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fintech', 
        'USER': 'postgres', 
        'PASSWORD':'admin123',  
        'HOST': 'localhost', 
        'PORT': '5432',
    }
}

AUTH_USER_MODEL = 'accountapp.User'
REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'error',
    # 'DATE_INPUT_FORMATS': [("%d /%m/%Y"),],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}




# REST_FRAMEWORK = {
#     'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
# }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

from datetime import timedelta
import datetime

SIMPLE_JWT = {
'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
'REFRESH_TOKEN_LIFETIME': timedelta(days=20),
'ROTATE_REFRESH_TOKENS': False,

}

# REST_FRAMEWORK = {
#     "DATE_INPUT_FORMATS": ["%d-%m-%Y"],
    
# }
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

#use only server deployment

# EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'email-smtp.ap-south-1.amazonaws.com'
# # SENDER='sunilv969572@gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587

# # EMAIL_HOST_USER = 'sunilv969572@gmail.com'
# EMAIL_HOST_USER = 'AKIAWI2PDRYP7BFYEHGK'
# EMAIL_HOST_PASSWORD = 'BN6WK5lmfQGS+0+1jLFO5yK81cGXKZxAYd7SE4eiOxx2'


#use only local side
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER ='staff.ddspl@gmail.com'
EMAIL_HOST_PASSWORD ='Digital@123'
