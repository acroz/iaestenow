#!/usr/bin/env python3

import json
from iaestenow import database as db
from iaestenow import facebook

def init():
    """Create the schema"""
    db.Base.metadata.create_all(db.engine)

def populate():
    """
    Temporary for development: Populate some data
    """

    session = db.Session()
    
    locs = [db.Location(address='London, UK', latitude=51.5072, longitude=0),
            db.Location(address='Graz',       latitude=47.0667, longitude=15.4333),
            db.Location(address='Utrecht',    latitude=52.0833, longitude=5.1167),
            db.Location(address='Nürnberg',   latitude=49.4500, longitude=11.0833),
            db.Location(address='München',    latitude=48.1333, longitude=11.5667)]
    session.add_all(locs)

    entrytypes = [db.EntryType(name='event'),
                  db.EntryType(name='conference'),
                  db.EntryType(name='reception weekend'),
                  db.EntryType(name='twitter')]
    session.add_all(entrytypes)
    
    entries = [db.Entry(name='München Wochenende', location=locs[4], type=entrytypes[2]),
               db.Entry(name='User posted...', location=locs[3], type=entrytypes[3]),
               db.Entry(name='CONNECT', location=locs[2], type=entrytypes[1])] 
    session.add_all(entries)

    users = [db.User(name='Andrew Crozier', email='wacrozier@gmail.com', password='password'),
             db.User(name='Pim Sauter', email='pim.sauter@gmail.com', password='password')]
    session.add_all(users)

    session.commit()

init()
populate()

# Load settings file    
with open('settings.json') as fp:
    settings = json.load(fp)
    
facebook.init(settings['facebook']['id'], settings['facebook']['secret'])
facebook.populate()
