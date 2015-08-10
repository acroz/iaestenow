#!/usr/bin/env python3

import os
import json
from iaestenow import app, database, facebook

# Load settings file    
with open('settings.json') as fp:
    settings = json.load(fp)

app.secret_key = settings['secret_key']
    
# Run the flask app in debug mode
app.run(debug=True)
