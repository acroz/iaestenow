"""
Define the database interface with SQLAlchemy.
"""

from iaestenow.app import db
from flask.ext.login import UserMixin

ENTRY_TYPES = ['event',
               'conference',
               'reception weekend',
               'twitter']

HOSTING_STATUSES = [('no',    'No'),
                    ('maybe', 'Maybe'),
                    ('yes',   'Yes')]
HOSTING_STATUS_KEYS = [p[0] for p in HOSTING_STATUSES]

class User(db.Model, UserMixin):
    """
    Store users.
    """

    __tablename__ = 'users'

    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String)
    password = db.Column(db.String)
    name     = db.Column(db.String)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    hosting  = db.Column(db.Enum(*HOSTING_STATUS_KEYS), default='no')

    location = db.relationship('Location', backref=db.backref('users', order_by=id))

class Location(db.Model):
    """
    Store address-coordinate information in the database.
    """

    __tablename__ = 'locations'

    id        = db.Column(db.Integer, primary_key=True)
    address   = db.Column(db.String)
    latitude  = db.Column(db.Float)
    longitude = db.Column(db.Float)
    facebook_id = db.Column(db.Integer)

    def __str__(self):
        return self.address

class Entry(db.Model):
    """
    Store entries in the database.
    """

    __tablename__ = 'entries'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.Enum(*ENTRY_TYPES))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    facebook_id = db.Column(db.Integer)

    location = db.relationship('Location', backref=db.backref('entries', order_by=id))
