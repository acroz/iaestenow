
from flask_wtf import Form
from wtforms import StringField, PasswordField, validators

class RegistrationForm(Form):
    email    = StringField('Email', [validators.Email()])
    password = PasswordField('Password', [validators.Length(min=6)])
    name     = StringField('Full Name', [validators.InputRequired()])

class LoginForm(Form):
    email    = StringField('Email', [validators.Email()])
    password = PasswordField('Password', [validators.Length(min=6)])

class ProfileForm(Form):
    name     = StringField('Full Name', [validators.InputRequired()])
    password = PasswordField('Password', [validators.Length(min=6)])
