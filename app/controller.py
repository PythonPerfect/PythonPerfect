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

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

#Update
#No update support

#Delete
def delete_user(user):
    delete_from_database(user)

def delete_user_by_id(user_id):
    u = get_user_by_userid(user_id)
    delete_from_database(u)

def delete_user_by_username(username):
    u = get_user_by_username(username)
    delete_from_database(u)

def delete_user_by_email(email):
    u = get_user_by_email(email)
    delete_from_database(u)

def delete_all_users():
    users = get_all_user()
    for u in users:
        delete_from_database(u)

#-----For Course Model-----
#Creation
def add_new_course(title):
    course = Course(title=title)
    add_to_database(course)
    return course

#Read
def get_all_courses():
    return Course.query.all()

def get_course_by_title(title):
    return Course.query.filter_by(title=title).first()

def get_course_by_id(course_id):
    return Course.query.filter_by(id=course_id).first()

#Update
#No update support

#Delete
def delete_course_by_id(course_id):
    if (Content.query.filter(Content.course.has(id=course_id)).first() is not None and
            Quiz.query.filter(Quiz.course.has(id=course_id)).first() is not None):
        raise RowNotEmpty

    u = get_course_by_id(course_id)
    delete_from_database(u)

def delete_course_by_title(title):
    if (Content.query.filter(Content.course.has(title=title)).first() is not None and
            Quiz.query.filter(Quiz.course.has(title=title)).first() is not None):
        raise RowNotEmpty

    u = get_course_by_title(title)
    delete_from_database(u)

def delete_all_course():
    if (Content.query.first() is not None and
            Quiz.query.first() is not None):
        raise RowNotEmpty

    courses = get_all_courses
    for cor in courses:
        delete_from_database(cor)


#-----For Content Model-----
#Creation
def add_new_content(title, text, course):
    con = Content(title=title, text=text, course=course)
    add_to_database(con)
    return con


#Read
def get_all_content():
    return Content.query.all()

def get_content_by_id(content_id):
    return Content.query.filter_by(id=content_id).first()

def get_content_by_title(title):
    return Content.query.filter_by(title=title).first()

def get_content_by_course_n_title(course, title):
    return Content.query.filter(Content.course==course, Content.title==title).first()

def get_contents_by_course(course):
    return Content.query.filter(Content.course==course).all()

#Update
#No Update Support

#Delete
def delete_content(content):
    if Content_Viewed.query.filter(Content_Viewed.content == content).first() is not None:
        raise RowNotEmpty

    delete_from_database(content)

def delete_content_by_id(content_id):
    if Content_Viewed.query.filter(Content_Viewed.content.has(id=content_id)).first() is not None:
        raise RowNotEmpty

    con = get_content_by_id(content_id)
    delete_from_database(con)

def delete_content_by_title(title):
    if Content_Viewed.query.filter(Content_Viewed.content.has(title=title)).first() is not None:
        raise RowNotEmpty

    con = get_content_by_title(title)
    delete_from_database(con)

def delete_all_content_from_course(course):
    #Finds all Content_Viewed tied to course. 
    if Content_Viewed.query.filter(Content_Viewed.content.has(Content.course==course)).first() is not None:
        raise RowNotEmpty

    cons = get_contents_by_course(course)
    for con in cons:
        delete_from_database(con)

def delete_all_content():
    if Content_Viewed.query.first() is not None:
        raise RowNotEmpty

    cons = get_all_content()
    for con in cons:
        delete_from_database(con)

#-----For Quiz Model-----
#Creation
def add_new_quiz(title, course):
    q = Quiz(title=title, course=course)
    add_to_database(q)
    return q

#Read
def get_all_quiz():
    return Quiz.query.all()

def get_quiz_by_id(quiz_id):
    return Quiz.query.filter_by(id=quiz_id).first()

def get_quiz_by_title(title):
    return Quiz.query.filter_by(title=title).first()

def get_quiz_by_course_n_title(course, title):
    return Quiz.query.filter(Quiz.course==course, Quiz.title==title).first()

def get_quiz_by_course(course):
    return Quiz.query.filter(Quiz.course==course).all()

#Update
#No Update Support

#Delete
def delete_quiz(quiz):
    if Question.query.filter(Question.quiz == quiz).first() is not None:
        raise RowNotEmpty

    delete_from_database(quiz)

def delete_quiz_by_id(quiz_id):
    if Question.query.filter(Question.quiz.has(id==quiz_id)).first() is not None:
        raise RowNotEmpty

    q = get_quiz_by_id(quiz_id)
    delete_from_database(q)

def delete_quiz_by_title(title):
    if Question.query.filter(Question.quiz.has(title=title)).first() is not None: 
        raise RowNotEmpty

    q = get_quiz_by_title(title)
    delete_from_database(q)

def delete_all_quiz_from_course(course):
    if Question.query.filter(Question.quiz.has(Quiz.course==course)).first() is not None:
        raise RowNotEmpty

    qs = get_quiz_by_course(course)
    for q in qs:
        delete_from_database(q)

def delete_all_quiz():
    if Question.query.first() is not None:
        raise RowNotEmpty

    qs = get_all_quiz()
    for q in qs:
        delete_from_database(q)

#-----For Question Model-----
#Creation
def add_new_question(question, answer, quiz):
    que = Question(question=question, answer=answer, quiz=quiz)
    add_to_database(que)
    return que

#Read
def get_all_question():
    return Question.query.all()

def get_question_by_id(question_id):
    return Question.query.filter_by(id=question_id).first()

def get_question_by_quiz_n_question(quiz, question):
    return Question.query.filter(Question.quiz==quiz, Content.question==question).first()

def get_question_by_quiz(quiz):
    return Question.query.filter(Question.quiz==quiz).all()

#Update
#No Update supported

#Delete
def delete_question_by_id(question_id):
    if Question_Response.query.filter(Question_Response.question.has(id==question_id)) is not None:
        raise RowNotEmpty
    
    que = get_question_by_id(question_id)
    delete_from_database(que)

def delete_all_question_from_quiz(quiz):
    if Question_Response.query.filter(Question_Response.question.has(Question.quiz==quiz)).first() is not None:
        raise RowNotEmpty

    ques = get_question_by_quiz(quiz)
    for que in ques:
        delete_from_database(que)


def delete_all_question():
    if Question_Response.query.first() is not None:
        raise RowNotEmpty

    ques = get_all_question()
    for que in ques:
        delete_from_database(que)

#-----For Question_Response Model-----
#Creation
def add_new_question_response(response, question, user):
    q_r = Question_Response(response=response, question=question, user=user)
    add_to_database(q_r)
    return q_r

#Read
def get_user_question_response(user, question):
    return Question_Response.query.filter(Question_Response.question==question, Question_Response.user==user).first()

def get_all_question_response():
    return Question_Response.query.all()

#Update
#No update support as of yet for Question_Response

#Delete
def delete_question_response(user, question):
    q_r = get_user_question_response(user, question)
    delete_from_database(q_r)

def delete_all_question_response():
    q_rs = get_all_question_response()
    for q_r in q_rs:
        delete_from_database(q_r)

#-----For Content_Viewed Model-----
#Creation
def add_new_content_viewed(user, content):
    c_v = Content_Viewed(user=user, content=content)
    add_to_database(c_v)
    return c_v

#Read
def get_user_content_viewed(user, content):
    return Content_Viewed.query.filter(Content_Viewed.content==content, Content_Viewed.user==user).first()

def get_all_content_viewed():
    return Content_Viewed.query.all()

#Update
#No update support as of yet for Content_Viewed

#Delete
def delete_user_content_viewed(user, content):
    c_v = get_user_content_viewed(user, content)
    delete_from_database(c_v)

def delete_all_content_viewed():
    c_vs = get_all_content_viewed()
    for c_v in c_vs:
        delete_from_database(c_v)