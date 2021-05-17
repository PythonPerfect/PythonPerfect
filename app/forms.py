from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo, Length, Regexp
from app.models import *

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
        Regexp(regex, message='Use 8 or more characters with a mix of letters and numbers and no special characters.')])

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


class AddCourseForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()])

    submit = SubmitField('Add')

    def validate_title(self, title):
        course = Course.query.filter_by(title = title.data).first()
        if course is not None:
            flash("Course already added. Please add another course.", "danger")
            raise ValidationError('Course already added. Please add another course.')
        elif not 4 <= len(title.data) <= 50:
            flash("The Course title must be at least 4 characters long and no more than 50 characters.", "danger") 
            raise ValidationError('The Course title must be at least 4 characters long and no more than 50 characters.')


class AddQuestionForm(FlaskForm):
    question = TextAreaField(
        'Question',
        validators=[DataRequired()])
    answer = StringField(
        'Answer',
        validators=[DataRequired()])

    submit = SubmitField('Add')

    def validate_question(self,question):
        question = Question.query.filter_by(question = question.data).all()


class AddContentForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()])

    submit = SubmitField('Add')

    def validate_title(self, title):
        content = Content.query.filter_by(title = title.data).first()
        if not 4 <= len(title.data) <= 50:
            flash("The Content title must be at least 4 characters long and no more than 50 characters.", "danger") 
            raise ValidationError('The Content title must be at least 4 characters long and no more than 50 characters.')

class AddQuizForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()])

    submit = SubmitField('Add')

    def validate_title(self, title):
        quiz = Quiz.query.filter_by(title = title.data).first()
        if not 4 <= len(title.data) <= 50:
            flash("The Quiz title must be at least 4 characters long and no more than 50 characters.", "danger") 
            raise ValidationError('The Quiz title must be at least 4 characters long and no more than 50 characters.')

class EditContentForm(FlaskForm):
    content = TextAreaField(
        'Content',
    )

    submit = SubmitField('Save')

    def validate_title(self, content):
        pass
            

class QuizQuestionForm(FlaskForm):
    answer = StringField(
        'Answer',
        validators=[DataRequired()])

    submit_next = SubmitField('Continue')
    submit_last = SubmitField('Finish')

    def validate_title(self):
        pass
class AdminRegistrationForm(RegistrationForm):
    specialPassword = PasswordField('Special Password', [DataRequired()])
