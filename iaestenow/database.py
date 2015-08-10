"""
Define the database interface with SQLAlchemy.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.login import UserMixin

# Using local file database for the moment
engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base, UserMixin):
    """
    Store users.
    """

    __tablename__ = 'users'

    id       = Column(Integer, primary_key=True)
    email    = Column(String)
    password = Column(String)
    name     = Column(String)

class Location(Base):
    """
    Store address-coordinate information in the database.
    """

    __tablename__ = 'locations'

    id        = Column(Integer, primary_key=True)
    address   = Column(String)
    latitude  = Column(Float)
    longitude = Column(Float)
    facebook_id = Column(Integer)

class EntryType(Base):
    """
    Store entry types in the database.
    """

    __tablename__ = 'entry_types'

    name = Column(String, primary_key=True)

class Entry(Base):
    """
    Store entries in the database.
    """

    __tablename__ = 'entries'

    id   = Column(Integer, primary_key=True)
    name = Column(String)
    location_id = Column(Integer, ForeignKey('locations.id'))
    type_id     = Column(String, ForeignKey('entry_types.name'))
    facebook_id = Column(Integer)

    location = relationship('Location', backref=backref('entries', order_by=id))
    type = relationship('EntryType', backref=backref('entries', order_by=id))
