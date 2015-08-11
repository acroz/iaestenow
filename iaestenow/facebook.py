
import requests
from iaestenow.models import db, Entry, Location

ACCESS_TOKEN = None

def graph_request(path, params={}):

    if ACCESS_TOKEN is not None:
        params['access_token'] = ACCESS_TOKEN

    return requests.get('https://graph.facebook.com/' + path,
                        params=params)

def init(app_id, app_secret):
    """
    Get and store a bearer token for this session.
    """
    
    response = graph_request('oauth/access_token',
                             params={'grant_type':    'client_credentials',
                                     'client_id':     app_id,
                                     'client_secret': app_secret})

    # Get access token from response
    assert response.text.startswith('access_token=')

    global ACCESS_TOKEN
    ACCESS_TOKEN = response.text[13:]

def recent_iaeste():

    if ACCESS_TOKEN is None:
        raise Exception('ACCESS_TOKEN not initialised')
   
    response = graph_request('iaestenl/events')

    return response.json()

def populate():

    for event in recent_iaeste()['data']:

        # See if entry exists
        event_id = int(event['id'])
        query = Entry.query.filter_by(facebook_id=event_id)
        if query.count() > 0:
            # Event already exists, don't need to do anythinf
            continue

        else:
            # Add the event
            
            # Does the event have a place assigned?
            if 'place' not in event:
                # Skip for now
                continue
            if 'id' not in event['place']:
                continue
            
            # See if the location exists
            loc_id = int(event['place']['id'])
            query = Location.query.filter_by(facebook_id=loc_id)
            if query.count() > 0:
                # Use existing location
                loc = query.one()
            else:
                # Create new location
                fb_location = event['place']['location']

                # Construct address as single string
                address = []
                for key in ['name', 'street', 'city', 'region', 'state', 'country']:
                    if key in fb_location:
                        address.append(fb_location[key])
                address = ', '.join(address)
                
                # Generate new location
                loc = Location(address=address,
                               latitude=fb_location['latitude'],
                               longitude=fb_location['longitude'],
                               facebook_id=loc_id)
                db.session.add(loc)

            entry = Entry(name=event['name'],
                          location=loc,
                          type='event')
        db.session.add(entry)
    db.session.commit()

if __name__ == '__main__':

    import json
    
    with open('settings.json') as fp:
        settings = json.load(fp)
    
    init(settings['facebook']['id'], settings['facebook']['secret'])
    print(json.dumps(recent_iaeste(), indent=2))
