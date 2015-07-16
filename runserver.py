#!/usr/bin/env python3

import os
from iaestenow import app, database

# Clear the database file if it exists
try:
    os.remove('test.db')
except FileNotFoundError:
    pass

# Populate the database
database.init()
database.populate()

# Run the flask app in debug mode
app.run(debug=True)
