"""
Create a flask app serving the webpage and JSON APIs.
"""

import flask
from iaestenow import geocode as geo
from iaestenow import entries as entr

# Create the flask app
app = flask.Flask(__name__)

@app.route('/')
def index():
    """Serve the main html page"""
    return flask.render_template('map.html')

@app.route('/geocode')
def geocode():
    """Provide a cached geocode service"""
    address = flask.request.args.get('address', '', type=str)
    data = geo.geocode_dict(address)
    return flask.jsonify(**data)

@app.route('/entries')
def entries():
    """Provide a list of map entries"""
    data = entr.entries_dict()
    return flask.jsonify(response=data)
