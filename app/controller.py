from flask_sqlalchemy import model
from app import db
from app.models import *

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class RowNotEmpty(Error):
    """Raised when the row not empty"""

def add_to_database(item):
    db.session.add(item)
    db.session.commit()

def delete_from_database(item):
    db.session.delete(item)
    db.session.commit()

#-----For Users Model-----
#Creation
def add_new_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    add_to_database(user)
    return user

def add_new_admin(username, email, password):
    admin = User(username=username, email=email, admin=True)
    admin.set_password(password)
    add_to_database(admin)
    return admin

#Read
def get_all_user():
    return User.query.all()

def get_admins():
    return User.query.filter_by(admin=True).all()

def get_nonadmins():
    return User.query.filter_by(admin=False).all()

def get_user_by_userid(user_id):
    return User.query.filter_by(id=user_id).first()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_emial(email):
    return User.query.filter_by(email=email).first()

#Update
#No update support as of yet for users

#Delete
def delete_user_by_id(user_id):
    u = get_user_by_userid(user_id)
    delete_from_database(u)

def delete_user_by_username(username):
    u = get_user_by_username(username)
    delete_from_database(u)

def delete_all_users():
    users = get_all_user()
    for u in users:
        delete_from_database(u)

#-----For Course Model-----
#Creation
def add_new_course(title):
    course = Course(titel=title)
    add_to_database(course)

#Read
def get_all_courses():
    return Course.query.all()

def get_course_by_title(title):
    return Course.query.filter_by(title=title).first()

def get_coruse_by_id(course_id):
    return Course.query.filter_by(id=course_id).first()

#Update
#No update support as of yet for course

#Delete
def delete_course_by_id(course_id):
    if Course.query.firs() != None:
        return 
    u = get_coruse_by_id(course_id)
    delete_from_database(u)

def delete_course_by_title(title):
    u = get_course_by_title(title)
    delete_from_database(u)

#-----For Content Model-----
#Creation
def add_new_content(title, text, course):
    con = Content(title=title, text=text, course=course)
    add_to_database(con)

#Read
def get_all_content():
    return Content.query.all()

def get_content_by_id(content_id):
    return Content.query.filter_by(id=content_id).first()

def get_content_by_title(title):
    return Content.query.filter_by(title=title).first()

def get_contents_by_course(course):
    return Content.query.filter(Content.course==course).all()

#Delete
def delete_content_by_id(course_id):
    con = get_content_by_id(course_id)
    delete_from_database(con)

def delete_content_by_title(title):
    con = get_content_by_title(title)
    delete_from_database(con)

def delete_all_content_from_course(course):
    cons = get_contents_by_course(course)
    for con in cons:
        delete_from_database(con)

#-----For Question_Response Model-----
#Creation

#Read
def get_user_response(user, question):
    return Question_Response.query.filter(Question_Response.question==question, Question_Response.user==user).first()

#Update
#No update support as of yet for Question_Response

#Delete

#-----For Content_Viewed Model-----
#Creation

#Read
def get_user_content_viewed(user, content):
    return Content_Viewed.query.filter(Content_Viewed.content==content, Content_Viewed.user==user).first()

#Update
#No update support as of yet for Content_Viewed

#Delete