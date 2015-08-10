"""
Create a flask app serving the webpage and JSON APIs.
"""

import flask
from iaestenow import geocode as geo
from iaestenow import entries as entr
from iaestenow.login import loginmanager, register_user
from flask.ext import login as fl
from iaestenow import forms
from iaestenow.database import Session, User
from sqlalchemy.orm.exc import NoResultFound

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm(flask.request.form)

    if flask.request.method == 'POST' and form.validate():
        session = Session()
        query = session.query(User).filter_by(email=form.email.data)

        try:
            fl.login_user(query.one())
        except NoResultFound:
            flask.flash('No user account with those credentials found.')
        else:
            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')
            #if not next_is_valid(next):
            #    return flask.abort(400)

            return flask.redirect(next or flask.url_for('index'))

    return flask.render_template('login.html', form=form)

@app.route('/profile')
@fl.login_required
def profile_edit():
    form = forms.ProfileForm(flask.request.form, fl.current_user)
    #if flask.request.method == 'POST' and form.validate():
        
    return flask.render_template('profile-edit.html', form=form)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    session = Session()
    query = session.query(User).filter_by(id=int(user_id))
    try:
        user = query.one()
    except NoResultFound:
        flask.abort(404)
    return flask.render_template('profile.html', user=user)
