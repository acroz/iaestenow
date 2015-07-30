
if __name__ == '__main__':
    import sys
    # Remove script dir from path
    sys.path = sys.path[1:]

import twitter

BEARER_TOKEN = None

def init(consumer_key, consumer_secret):
    """
    Get and store a bearer token for this session.
    """
    global BEARER_TOKEN
    BEARER_TOKEN = twitter.oauth2_dance(consumer_key, consumer_secret)

def recent_iaeste(number=25):
    """
    Get recent tweets with the #IAESTE hashtag.
    """

    if BEARER_TOKEN is None:
        raise Exception('BEARER_TOKEN not initialised')

    # Open connection
    t = twitter.Twitter(auth=twitter.OAuth2(bearer_token=BEARER_TOKEN))

    # Search
    results = t.search.tweets(q='#IAESTE -RT', count=number)

    return results['statuses']

if __name__ == '__main__':

    import json
    
    with open('settings.json') as fp:
        settings = json.load(fp)
    
    init(settings['twitter']['key'], settings['twitter']['secret'])

    for tweet in recent_iaeste():
        tpl = 'Tweet: {}\ngeo: {}\nplace: {}\nuserloc: {}\n'
        print(tpl.format(tweet['text'], str(tweet['geo']),
                         str(tweet['place']), str(tweet['user']['location'])))
