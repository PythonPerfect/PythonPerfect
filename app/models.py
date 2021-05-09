from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)

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

    def __repr__(self):
        return '<Course {}>'.format(self.title)

class Content(db.Model):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    course_id = db.Column(db.Integer)
    title = db.Column(db.String(50))
    text = db.Column(db.Text)

    def __repr__(self):
        return '<Content {}>'.format(self.title)
