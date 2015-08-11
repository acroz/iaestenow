"""
Query the database and provide a list of map entries.
"""

from iaestenow.models import Entry

def entries():
    """
    Get entries from the database.
    """
    return Entry.query.all()

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
    print(data)
    return data
