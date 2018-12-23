from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username or Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    login = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 30)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(6, 60)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 30)])
    password2 = PasswordField('Confirm password', validators=[DataRequired(),
                              EqualTo('password', message='Password do not match.')])
    register = SubmitField('Register')
