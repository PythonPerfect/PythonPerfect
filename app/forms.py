from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo, Length, Regexp
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(),
        Length(min=4, max=20, message='Must be at least 4 and less than 20 characters!')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,128}$"
    password = PasswordField(
        'Password',
        validators=[DataRequired(),
        Regexp(regex, message='Use 8 or more characters with a mix of letters and numbers')])
    re_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken, please use a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Email already registered, use a different one.')