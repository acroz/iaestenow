
import flask
from flask.ext import login as fl

from iaestenow.app import app, db, loginmanager
from iaestenow.models import User

from iaestenow import geocode as geo
from iaestenow import entries as entr
from iaestenow import forms

from sqlalchemy.orm.exc import NoResultFound

@loginmanager.user_loader
def load_user(userid):

    userid = int(userid)

    query = User.query.filter_by(id=userid)

    if query.count() == 1:
        return query.one()
    else:
        return None

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
        new = User(email=form.email.data,
                   password=form.password.data,
                   name=form.name.data)
        db.session.add(new)
        db.session.commit()
        flask.flash('Registration successful.')
    return flask.render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm(flask.request.form)

    if flask.request.method == 'POST' and form.validate():
        query = User.query.filter_by(email=form.email.data)

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

@app.route('/logout')
@fl.login_required
def logout():
    fl.logout_user()
    flask.flash('Logged out.')
    return flask.redirect(flask.url_for('index'))

@app.route('/profile/', methods=['GET', 'POST'])
@fl.login_required
def profile_edit():
    user = fl.current_user
    form = forms.ProfileForm(flask.request.form, user)
    if flask.request.method == 'POST' and form.validate():
        user.name = form.name.data
        user.password = form.password.name
        db.session.add(user)
        db.session.commit()
        flask.flash('Profile updated.')
    return flask.render_template('profile-edit.html', form=form)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    query = User.query.filter_by(id=int(user_id))
    try:
        user = query.one()
    except NoResultFound:
        flask.abort(404)
    return flask.render_template('profile.html', user=user)
