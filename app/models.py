from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import false, true
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)

    #Backref
    question_responses = db.relationship('Question_Response',
                                          backref='user',
                                          lazy='dynamic',
                                          cascade="all, delete",
                                          passive_deletes=True)
    contents_viewed = db.relationship('Content_Viewed',
                                       backref='user',
                                       lazy='dynamic',
                                       cascade="all, delete",
                                       passive_deletes=True)
    results = db.relationship('Result',
                               backref='user',
                               lazy='dynamic',
                               cascade="all, delete",
                               passive_deletes=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Course(db.Model):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    title = db.Column(db.String(50), index=True, unique=True)

    #Backref
    contents = db.relationship('Content', backref='course', lazy='dynamic')
    quizzes = db.relationship('Quiz', backref='course', lazy='dynamic')

    def __repr__(self):
        return '<Course {}>'.format(self.title)

class Content(db.Model):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    title = db.Column(db.String(50), index=True)
    text = db.Column(db.Text)

    #Foreign Key
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    #Backref
    contents_viewed = db.relationship('Content_Viewed', backref='content', lazy='dynamic')

    def __repr__(self):
        return '<Content {}>'.format(self.title)

class Quiz(db.Model):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    title = db.Column(db.String(50), index=True)

    #Foreign Key
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    #Backref
    questions = db.relationship('Question', backref='quiz', lazy='dynamic')
    results = db.relationship('Result', backref='quiz', lazy='dynamic')

    def __repr__(self):
        return '<Quiz {}>'.format(self.id)

class Question(db.Model):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    question = db.Column(db.String(256), index=True)
    answer = db.Column(db.String(32))

    #Foreign Key
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    #Backref
    question_response = db.relationship('Question_Response', backref='question', lazy='dynamic')

    def __repr__(self):
        return '<Question {}>'.format(self.body)

class Question_Response(db.Model):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    response = db.Column(db.String(32))
    correct = db.Column(db.Boolean, default=False)

    #Foreign Key
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="cascade"))
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'))

    def __repr__(self):
        return '<Question_Response {}>'.format(self.response)

    def check_correct(self):
        return self.response == self.question.answer

class Content_Viewed(db.Model):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)

    #Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="cascade"))
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))

    def __repr__(self):
        return '<Content_Viewed {}>'.format(self.id)

class Result(db.Model):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    #Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="cascade"))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    #Backref
    question_response = db.relationship('Question_Response', backref='result', lazy='dynamic')

    def __repr__(self):
        return '<Result {}, {}>'.format(self.user_id, self.quiz_id)