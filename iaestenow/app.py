"""
Create a flask app serving the webpage and JSON APIs.
"""

import flask
from iaestenow import geocode as geo
from iaestenow import entries as entr
from iaestenow.login import loginmanager, load_user, register_user
from iaestenow import forms

# Create the flask app
app = flask.Flask(__name__)
loginmanager.init_app(app)

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm(flask.request.form)
    if flask.request.method == 'POST' and form.validate():
        register_user(form.email.data, form.password.data, form.name.data)
        flask.flash('Registration successful.')
    return flask.render_template('register.html', form=form)
