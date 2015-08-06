#!/usr/bin/env python3

import os
import json
from iaestenow import app, database, facebook

# Clear the database file if it exists
try:
    os.remove('test.db')
except FileNotFoundError:
    pass

# Load settings file    
with open('settings.json') as fp:
    settings = json.load(fp)
    
# Populate the database
database.init()
database.populate()

facebook.init(settings['facebook']['id'], settings['facebook']['secret'])
facebook.populate()

# Run the flask app in debug mode
app.run(debug=True)
