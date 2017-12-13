#!flask/bin/python

import config
config.DEBUG = False

from app import app
app.run(debug = False)
