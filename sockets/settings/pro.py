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
DEBUG = False

#==================================================Allowed Host==================================================
ALLOWED_HOSTS = ['hubursockets-env.eba-evsqtpnd.ap-southeast-1.elasticbeanstalk.com']

#==================================================Internationalization==================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dubai'