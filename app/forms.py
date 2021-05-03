from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    #ADD LENGTH VALIDATOR FOR USERNAME AND PASSWORD AFTER REGISTRATION PAGE IS DONE
    #ADD REGEXP VALIDATOR FOR USERNAME ADN PASSWORD TO ENSURE CORRECT FORMS
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')