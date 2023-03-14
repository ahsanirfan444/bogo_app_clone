from .base import *
import os

#==================================================DEBUG Settings==================================================
DEBUG = eval(os.getenv("DEBUG"))

#==================================================Admin Email configuration==================================================
SERVER_EMAIL = os.getenv("SERVER_EMAIL")
ADMINS = [('Ahsan Irfan','ahsan.irfan444@gmail.com'),('shahnawaz irfan', 'shahnawazmemon78@gmail.com')]
EMAIL_SUBJECT_PREFIX = "Hubur development error"


#==================================================Allowed Host==================================================

ALLOWED_HOSTS = ['dev-portal.huburway.com']

#==================================================S3 Bucket Configuration==================================================

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN")
AWS_LOCATION = 'media'
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
AWS_DEFAULT_ACL = 'public-read'


MEDIA_ROOT = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)


AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': os.getenv("CacheControl"),
    'ACL': 'public-read',
}


DEFAULT_FILE_STORAGE = 'hubur.storage_backends.MediaStorage'


#==================================================Database Configuration==================================================


# Development Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DEV_DB_NAME"),
        'USER': os.getenv("DEV_DB_USER"),
        'PASSWORD': os.getenv("DEV_DB_PASSWORD"),
        'HOST': os.getenv("DEV_DB_HOST"),
        'PORT': os.getenv("DEV_DB_PORT")
    }
}

#==================================================Middlewares==================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hubur_apis.middlewares.ExceptionMiddleware.ExceptionMiddleware',
    'hubur_apis.middlewares.HttpsRedirectMiddleware.WWWRedirectMiddleware'
]


#==================================================Static Files Settings==================================================

STATIC_URL = "/static/"
STATIC_ROOT = "static/"

#==================================================Email settings=================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = eval(os.getenv("EMAIL_USE_TLS"))
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")


#==================================================Internationalization==================================================
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE")
TIME_ZONE = os.getenv("TIME_ZONE")