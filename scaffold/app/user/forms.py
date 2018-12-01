from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email Address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(6, 40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 25)])
    confirm = PasswordField('Confirm password', validators=[DataRequired(),
                            EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')
