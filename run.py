#!flask/bin/python

import config
config.DEBUG = True

from app import app
app.run()
