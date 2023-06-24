from .base import *

#==================================================Middlewares========================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#==================================================DEBUG Settings==================================================
DEBUG = True

#==================================================Allowed Host==================================================
ALLOWED_HOSTS = ['*']

#==================================================Internationalization==================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'