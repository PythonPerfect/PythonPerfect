from flask import Flask, render_template, redirect, url_for, request, session, flash
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from werkzeug.urls import url_parse

@app.route("/deleting-user/<del_user_id>")
@login_required
def delete_user(del_user_id):
  if current_user.admin:
    user = User.query.filter_by(id = del_user_id).first()

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))

@app.route("/deleting-course/<del_course_id>")
@login_required
def delete_course(del_course_id):
  if current_user.admin:
    course = Course.query.filter_by(id = del_course_id).first()

    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route("/")
def index():
    return render_template("index.html", title="Python Perfect")

@app.route("/login", methods=["POST", "GET"])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    #ADD EMAIL LOGIN SUPPORT LATER
    user = User.query.filter_by(username = form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=False)
    page_next = request.args.get('next')
    if not page_next or url_parse(page_next).netloc != '':
      page_next = url_for('dashboard')
    return redirect(page_next)
  return render_template('login.html', title='Sign In', form=form)

@app.route("/signup", methods=["POST", "GET"])
def signup():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data, admin=form.admin.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()

    login_user(user, remember=False)
    flash('Welcome, registration complete!')
    return redirect(url_for('dashboard'))
  return render_template('signup.html', title='Signup', form=form)

@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
  form = AddCourseForm()
  if form.validate_on_submit():
    course = Course(title=form.title.data)
    db.session.add(course)
    db.session.commit()

  all_courses = Course.query.all()
  return render_template("dashboard.html", title="Dashboard", form=form, courses=all_courses)


@app.route("/course/<course_id>", methods=["POST", "GET"])
@login_required
def course(course_id):
  form_content = AddContentForm()
  course = Course.query.filter_by(id = course_id).first()
  if form_content.validate_on_submit():
    content = Content.query.filter_by(course_id = course_id).filter_by(title=form_content.title.data).first()
    if content is not None:
      flash("Content already added.")
    else:
      content = Content(title=form_content.title.data, course_id=course_id, text="")
      db.session.add(content)
      db.session.commit()

  all_content = Content.query.filter(Content.course==course).all()
  all_quiz = Quiz.query.filter(Quiz.course==course).all()
  if course is not None:
    return render_template("course.html", course=course, title=course.title, form_content=form_content, all_content=all_content, all_quiz = all_quiz)
  else:
    return redirect(url_for('error404'))

@app.route("/edit-content/<content_id>", methods=["POST", "GET"])
@login_required
def edit_content(content_id):
  if not current_user.admin:
    return redirect(url_for('dashboard'))
  form = EditContentForm()
  content = Content.query.filter_by(id = content_id).first()
  if content.text:
    form.content.data = str(content.text)

  return render_template("edit-content.html", form=form, content=content, title=content.title)

@app.route("/edited/<content_id>", methods=["POST", "GET"])
@login_required
def edited(content_id):
  form = EditContentForm()
  content = Content.query.filter_by(id = content_id).first()
  if form.validate_on_submit():
    content.text = form.content.data
    db.session.commit()
  
  print(content.text)

  return redirect(url_for('edit_content', content_id = content.id))


@app.route("/view-content/<content_id>")
@login_required
def view_content(content_id):
  content = Content.query.filter_by(id = content_id).first()

  return render_template("view-content.html", content=content, title=content.title)


@app.route("/profile")
@login_required
def profile():
  return render_template("profile.html", title="Profile", user=current_user, courses=["Test 1", "Test 2"])


@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.errorhandler(404)
@app.route("/404")
def error404(error=404):
  return render_template("error404.html", title="Page Not Found")


@app.route("/users")
def users():
  if current_user.is_authenticated and current_user.admin:
    users = User.query.all()
    return render_template("users.html", users=users)
  else:
    return redirect(url_for('dashboard'))

@app.route("/quiz/<quiz_id>" , methods=["POST","GET"])
@login_required
def quiz(quiz_id):
  form = AddQuestionForm()
  quiz = Quiz.query.filter_by(id = quiz_id).first()
  if current_user.admin and form.validate_on_submit:
    question = Question.query.filter_by(quiz_id = quiz_id).filter_by(question=form.question.data).first()
    if question is not None:
      flash("Question already added")
    else:
      question = Question(question=form.question.data, answer=form.answer.data, quiz=quiz)
      db.session.add(question)
      db.session.commit
  all_questions = Question.query.filter_by(quiz_id = quiz_id).all()
  if question is not None:
    return render_template("edit-quiz.html", form=form, questions = all_questions)
  else:
    return redirect(url_for('error404'))



# FOR TESTING PURPOSES ONLY
@app.route("/delhalfusers")
def delete_all_users():
  x = input("Please confirm you want to delete all users: ")
    
  if x == "confirm":
    users = User.query.all()
    import math
    num = math.ceil(len(users) / 2)
    for i in range(num):
      u = users[i]
      db.session.delete(u)
      db.session.commit()
  return redirect(url_for('index'))

@app.route("/delhalfcourses")
def delete_all_courses():
  x = input("Please confirm you want to delete all courses: ")
    
  if x == "confirm":
    users = Course.query.all()
    import math
    num = math.ceil(len(users) / 2)
    for i in range(num):
      u = users[i]
      db.session.delete(u)
      db.session.commit()
  return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)