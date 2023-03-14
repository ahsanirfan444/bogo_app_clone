from .base import *
import tempfile
import os

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

#==================================================Email Backend==================================================


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#==================================================Hosts==================================================

ALLOWED_HOSTS = ['*']


#==================================================Database=================================================

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(tempfile.gettempdir(), 'hubur_local.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("LOCAL_DB_NAME"),
        'USER': os.getenv("LOCAL_DB_USER"),
        'PASSWORD': os.getenv("LOCAL_DB_PASSWORD"),
        'HOST': os.getenv("LOCAL_DB_HOST"),
        'PORT': os.getenv("LOCAL_DB_PORT")
    }
}

#==================================================Static Files directory==================================================

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]

# STATIC_ROOT = "static/"


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