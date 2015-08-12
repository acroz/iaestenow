#!/usr/bin/env python3

import json
from iaestenow.app import app, db
from iaestenow.models import Location, Entry, User
from iaestenow import facebook

def init():
    """Create the schema"""
    db.create_all()

def populate():
    """
    Temporary for development: Populate some data
    """

    locs = [Location(address='London, UK', latitude=51.5072, longitude=0),
            Location(address='Graz',       latitude=47.0667, longitude=15.4333),
            Location(address='Utrecht',    latitude=52.0833, longitude=5.1167),
            Location(address='Nürnberg',   latitude=49.4500, longitude=11.0833),
            Location(address='München',    latitude=48.1333, longitude=11.5667)]
    db.session.add_all(locs)
    db.session.commit()
    
    entries = [Entry(name='München Wochenende', location=locs[4], type='reception weekend'),
               Entry(name='User posted...', location=locs[3], type='twitter'),
               Entry(name='CONNECT', location=locs[2], type='conference')] 
    db.session.add_all(entries)
    db.session.commit()

    users = [User(name='Andrew Crozier', email='wacrozier@gmail.com',
                  password='password', location=locs[1], hosting='yes'),
             User(name='Pim Sauter', email='pim.sauter@gmail.com',
                  password='password', location=locs[2])]
    db.session.add_all(users)

    db.session.commit()

init()
populate()

# Load settings file    
with open('settings.json') as fp:
    settings = json.load(fp)
    
facebook.init(settings['facebook']['id'], settings['facebook']['secret'])
facebook.populate()
