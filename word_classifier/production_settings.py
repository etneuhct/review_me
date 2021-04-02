import django_heroku
from .settings import *

# Security (SSL)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

django_heroku.settings(locals(), databases=False)
