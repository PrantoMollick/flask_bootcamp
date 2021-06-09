# app/forms.py
"""
A form class simply defines the fields of the form as class variables.
"""

from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=10)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5, max=10)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

