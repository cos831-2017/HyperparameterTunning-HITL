# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# Redis setup
RDB_RESULTS_HOST = 'localhost'
RDB_RESULTS_PORT = 6379
RDB_RESULTS_NO = 1

# MonetDB setup

MONEDB_USERNAME = "admin"
MONETDB_PASSWORD = "monetdb"
MONETDB_HOST = "localhost"
MONEDB_PROV_DB ="prov"

# email server
MAIL_SERVER = 'your.mailserver.com'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# available languages
LANGUAGES = {
    'en': 'English',
}

# administrator list
ADMINS = ['you@example.com']
