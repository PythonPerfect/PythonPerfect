from flask import Flask, render_template, redirect, url_for, request, session, flash
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from werkzeug.urls import url_parse
from app.controller import *

# Landing page
@app.route("/")
def index():
  if current_user.is_authenticated:
    return redirect(url_for('dashboard'))
  return render_template("index.html", title="Python Perfect")

# Error Page
@app.errorhandler(404)
@app.route("/404")
def error404(error=404):
  return render_template("error404.html", title="Page Not Found")

# Login related routes
# -----------------------------------------------------------------------------
@app.route("/login", methods=["POST", "GET"])
def login():
  if current_user.is_authenticated:
    flash('Already logged in', 'info')
    return redirect(url_for('dashboard'))

  form = LoginForm()
  if form.validate_on_submit():
    #ADD EMAIL LOGIN SUPPORT LATER
    user = get_user_by_username(form.username.data)
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password', 'danger')
      return redirect(url_for('login'))
    login_user(user, remember=False)
    page_next = request.args.get('next')

    if not page_next or url_parse(page_next).netloc != '':
      page_next = url_for('dashboard')
      flash('Login successful', 'success')
    return redirect(page_next)
  return render_template('login.html', title='Sign In', form=form)


@app.route("/signup", methods=["POST", "GET"])
def signup():
  if current_user.is_authenticated:
    flash('Already logged in', 'info')
    return redirect(url_for('dashboard'))

  form = RegistrationForm()
  if form.validate_on_submit():
    user = add_new_user(form.username.data, form.email.data, form.password.data)
    login_user(user, remember=False)
    flash('Welcome, registration complete!', 'success')
    return redirect(url_for('dashboard'))
  return render_template('signup.html', title='Signup', form=form)

@app.route("/registerAdmin", methods=["POST", "GET"])
def registerAdmin():
  if current_user.is_authenticated:
    flash('Already logged in', 'info')
    return redirect(url_for('dashboard'))
  
  form = AdminRegistrationForm()
  
  if form.validate_on_submit():
    if app.config["ADMIN_KEY"]==form.specialPassword.data:
      user = add_new_admin(form.username.data, form.email.data, form.password.data)
      login_user(user, remember=False)
      flash('Welcome, registered as an Admin!', 'success')
      return redirect(url_for('dashboard'))
    else:
      flash('Incorrect Admin key', 'danger')
  return render_template('signup.html', title='Signup', form=form)


@app.route("/logout")
@login_required
def logout():
  logout_user()
  flash('Logged out succesfully', 'success')
  return redirect(url_for('index'))
# -----------------------------------------------------------------------------

# Dashboard
@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
  form = AddCourseForm()
  if form.validate_on_submit():
    add_new_course(form.title.data)
  all_courses = Course.query.all()
  return render_template("dashboard.html", title="Dashboard", form=form, courses=all_courses)

# Course related routes
# -----------------------------------------------------------------------------
@app.route("/course/<course_id>", methods=["POST", "GET"])
@login_required
def course(course_id):
  course=get_course_by_id(course_id)
  form_content = AddContentForm()
  form_quiz = AddQuizForm()
  
  all_content = get_contents_by_course(course)
  all_quiz = get_quiz_by_course(course)
  
  if course is not None:
    return render_template("course.html", course=course, title=course.title, form_content=form_content, form_quiz=form_quiz, all_content=all_content, all_quiz = all_quiz)
  else:
    return redirect(url_for('error404'))

@app.route("/course/content/add/<course_id>", methods=["POST", "GET"])
def add_content(course_id):
  form_content = AddContentForm()
  if form_content.validate_on_submit():
    content = Content.query.filter_by(course_id = course_id).filter_by(title=form_content.title.data).first()
    if content is not None:
      flash("Content already added.", 'info')
    else:
      content = Content(title=form_content.title.data, course_id=course_id, text=form_content.title.data)
      db.session.add(content)
      db.session.commit()
  return redirect(url_for('course', course_id = course_id))

@app.route("/course/quiz/add/<course_id>", methods=["POST", "GET"])
def add_quiz(course_id):
  form_quiz = AddQuizForm()
  if form_quiz.validate_on_submit():
    quiz = Quiz.query.filter_by(course_id = course_id).filter_by(title=form_quiz.title.data).first()
    if quiz is not None:
      flash("Quiz already added.", 'info')
    else:
      quiz = Quiz(title=form_quiz.title.data, course_id=course_id)
      db.session.add(quiz)
      db.session.commit()
  return redirect(url_for('course', course_id = course_id))
# -----------------------------------------------------------------------------

# Content related routes
# -----------------------------------------------------------------------------
@app.route("/content/edit/<content_id>", methods=["POST", "GET"])
@login_required
def edit_content(content_id):
  if not current_user.admin:
    return redirect(url_for('dashboard'))
  form = EditContentForm()
  content = get_content_by_id(content_id)
  if content.text:
    form.content.data = str(content.text)

  return render_template("edit-content.html", form=form, content=content, title=content.title)

@app.route("/content/edited/<content_id>", methods=["POST", "GET"])
@login_required
def edited_content(content_id):
  form = EditContentForm()
  content = get_content_by_id(content_id)
  if form.validate_on_submit():
    content.text = form.content.data
    db.session.commit()
    flash('Edits saved successfully!', 'success')

  return redirect(url_for('edit_content', content_id = content.id))


@app.route("/content/view/<content_id>")
@login_required
def view_content(content_id):
  content = get_content_by_id(content_id)

  return render_template("view-content.html", content=content, title=content.title)
# -----------------------------------------------------------------------------

# Quiz related routes
# -----------------------------------------------------------------------------
@app.route("/quiz")
@login_required
def quiz():
  form = QuizQuestionForm()
  return render_template("quiz.html", title="Quiz", user=current_user, form=form)

@app.route("/quiz/edit/<quiz_id>" , methods=["POST","GET"])
@login_required
def edit_quiz(quiz_id):
  form = AddQuestionForm()
  quiz = get_quiz_by_id(quiz_id)
  
  if current_user.admin and form.validate_on_submit():
    question = get_question_by_quiz_n_question(quiz, form.question.data)
    if question is not None:
      flash("Question already added")
    else:
      add_new_question(form.question.data, form.answer.data, quiz)
  all_questions = get_question_by_quiz(quiz)
  if quiz is not None:
    return render_template("edit-quiz.html", form=form, questions = all_questions)
  else:
    return redirect(url_for('error404'))
# -----------------------------------------------------------------------------

# Profile
@app.route("/profile")
@login_required
def profile():
  return render_template("profile.html", title="Profile", user=current_user, courses=["Test 1", "Test 2"])

# Users
@app.route("/users")
def users():
  if current_user.is_authenticated and current_user.admin:

    users = User.query.filter_by(admin=False)
    admins = User.query.filter_by(admin=True)

    return render_template("users.html", users=users, admins=admins)
  else:
    return redirect(url_for('dashboard'))


# Deleting related routes
# -----------------------------------------------------------------------------
@app.route("/delete/user/<del_user_id>")
@login_required
def delete_user(del_user_id):
  if current_user.admin:
    delete_user_by_id(del_user_id)
    return redirect(url_for('users'))

@app.route("/delete/course/<del_course_id>")
@login_required
def delete_course(del_course_id):
  if current_user.admin:
    try:
      delete_course_by_id(del_course_id)
      flash('Course delete successful', "success")
      return redirect(url_for('dashboard'))
    except RowNotEmpty:
      flash('Course cannot be deleted. Remove all content and quizzes before deleting.', "danger" )
  return redirect(url_for('dashboard'))
# -----------------------------------------------------------------------------

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