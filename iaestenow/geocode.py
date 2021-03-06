"""
A locally cached geocoding service.
"""

from iaestenow.models import db, Location
from geopy.geocoders import GoogleV3

def geocode(address):
    """
    Query the database for cached geocoding, and query Google if not found.
    """

    # Make sure a string
    address = str(address)

    # See first if it exists in cache
    query = Location.query.filter(Location.address == address)

    if query.count() > 0:
        return query[0]

    lat, lng = google(address)
    new_location = Location(address=address,
                            latitude=lat,
                            longitude=lng)
    db.session.add(new_location)
    db.session.commit()

    return new_location

def geocode_dict(address):
    """
    Return a dict with the geocode API information. 
    """
    code = geocode(address)
    return {'address':   code.address,
            'latitude':  code.latitude,
            'longitude': code.longitude}

def google(address):
    """
    Geocode an address with Google.
    """
    coder = GoogleV3()
    result = coder.geocode(address)
    return result.latitude, result.longitude
