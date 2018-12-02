from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,)
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SigninForm(FlaskForm):

    username = StringField('Username or Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    signin = SubmitField('Signin')


class SignupForm(FlaskForm):

    username = StringField('Username:', validators=[DataRequired(), Length(2, 30)])
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(max=60)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8)])
    password_2 = PasswordField(
        'Confirm Password:',
        validators=[EqualTo('password', message='Password do not match.')])
    signup = SubmitField('Signup')
