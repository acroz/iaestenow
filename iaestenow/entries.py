"""
Query the database and provide a list of map entries.
"""

from iaestenow.models import Entry, User

def entries():
    """
    Get entries from the database.
    """
    return Entry.query.all()

def user_locations():
    return User.query \
                .filter(User.location != None) \
                .filter(User.hosting != 'no').all()

def entries_dict():
    """
    Generate a dict containing the API data for an entries query.
    """
    data = []
    for entry in entries():
        data.append({
                'name': entry.name,
                'type': entry.type,
                'latitude': entry.location.latitude,
                'longitude': entry.location.longitude
            })
    for user in user_locations():
        data.append({
                'name': user.name,
                'type': 'user_location',
                'latitude': user.location.latitude,
                'longitude': user.location.longitude
            })
    return data
