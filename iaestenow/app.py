import os
import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

# Create the flask app
app = flask.Flask(__name__)

# Add the database
dirname = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dbfile = os.path.join(dirname, 'test.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
db = SQLAlchemy(app)

# Add the login manager
loginmanager = LoginManager()
loginmanager.init_app(app)
