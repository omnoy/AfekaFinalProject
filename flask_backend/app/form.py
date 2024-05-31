from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    email = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')