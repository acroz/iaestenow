"""
Define the database interface with SQLAlchemy.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Using local file database for the moment
engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Location(Base):
    """
    Store address-coordinate information in the database.
    """

    __tablename__ = 'locations'

    id        = Column(Integer, primary_key=True)
    address   = Column(String)
    latitude  = Column(Float)
    longitude = Column(Float)

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

    location = relationship('Location', backref=backref('entries', order_by=id))
    type = relationship('EntryType', backref=backref('entries', order_by=id))

def init():
    """Temporary for development: Create the schema"""
    Base.metadata.create_all(engine)

def populate():
    """
    Temporary for development: Populate some data
    """

    session = Session()
    
    locs = [Location(address='London, UK', latitude=51.5072, longitude=0),
            Location(address='Graz',       latitude=47.0667, longitude=15.4333),
            Location(address='Utrecht',    latitude=52.0833, longitude=5.1167),
            Location(address='Nürnberg',   latitude=49.4500, longitude=11.0833),
            Location(address='München',    latitude=48.1333, longitude=11.5667)]
    session.add_all(locs)

    entrytypes = [EntryType(name='event'),
                  EntryType(name='conference'),
                  EntryType(name='reception weekend'),
                  EntryType(name='twitter')]
    session.add_all(entrytypes)
    
    entries = [Entry(name='München Wochenende', location=locs[4], type=entrytypes[2]),
               Entry(name='User posted...', location=locs[3], type=entrytypes[3]),
               Entry(name='CONNECT', location=locs[2], type=entrytypes[1])] 
    session.add_all(entries)

    session.commit()

if __name__ == '__main__':
    init()
    populate()

    session = Session()
    for r in session.query(Location).order_by(Location.latitude):
        print(r.searchterm)
