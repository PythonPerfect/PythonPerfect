from flask import Flask, render_template, redirect, url_for, request, session, flash
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from werkzeug.urls import url_parse
from app.controller import *

@app.route("/deleting-user/<del_user_id>")
@login_required
def delete_user(del_user_id):
  if current_user.admin:
    try:
      delete_user_by_id(del_user_id)
      flash('User delete successful')
      return redirect(url_for('users'))
    except RowNotEmpty:
      flash('User can not be deleted. No cascading delete support.')

@app.route("/deleting-course/<del_course_id>")
@login_required
def delete_course(del_course_id):
  if current_user.admin:
    try:
      delete_course_by_id(del_course_id)
      flash('Course delete successful')
      return redirect(url_for('users'))
    except RowNotEmpty:
      flash('Course can not be deleted. No cascading delete support.')

@app.route("/")
def index():
  if current_user.is_authenticated:
    return redirect(url_for('dashboard'))
  return render_template("index.html", title="Python Perfect")

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

@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
  form = AddCourseForm()
  if form.validate_on_submit():
    add_new_course(form.title.data)
  all_courses = Course.query.all()
  return render_template("dashboard.html", title="Dashboard", form=form, courses=all_courses)


@app.route("/course/<course_id>", methods=["POST", "GET"])
@login_required
def course(course_id):
  course=get_course_by_id(course_id)
  form_content = AddContentForm()
  form_quiz = AddQuizForm()
  
  # for adding content
  if form_content.submit.data and form_content.validate():
    content = get_content_by_course_n_title(course, form_content.title.data)
    if content is not None:
      flash("Content already added.", 'info')
    else:
      add_new_content(form_content.title.data, form_content.title.data, course)

  # for adding quizzes
  if form_quiz.submit.data and form_quiz.validate():
    quiz = get_quiz_by_course_n_title(course, form_quiz.title.data)
    if quiz is not None:
      flash("Quiz already added.", 'info')
    else:
      add_new_quiz(form_quiz.title.data, course)

  all_content = get_contents_by_course(course)
  all_quiz = get_quiz_by_course(course)
  if course is not None:
    return render_template("course.html", course=course, title=course.title, form_content=form_content, form_quiz=form_quiz, all_content=all_content, all_quiz = all_quiz)
  else:
    return redirect(url_for('error404'))

@app.route("/edit-content/<content_id>", methods=["POST", "GET"])
@login_required
def edit_content(content_id):
  if not current_user.admin:
    return redirect(url_for('dashboard'))
  form = EditContentForm()
  content = get_content_by_id(content_id)
  if content.text:
    form.content.data = str(content.text)

  return render_template("edit-content.html", form=form, content=content, title=content.title)

@app.route("/edited/<content_id>", methods=["POST", "GET"])
@login_required
def edited(content_id):
  form = EditContentForm()
  content = get_content_by_id(content_id)
  if form.validate_on_submit():
    content.text = form.content.data
    db.session.commit()
    flash('Edits saved successfully!', 'success')
  
  print(content.text)

  return redirect(url_for('edit_content', content_id = content.id))


@app.route("/view-content/<content_id>")
@login_required
def view_content(content_id):
  content = get_content_by_id(content_id)

  return render_template("view-content.html", content=content, title=content.title)


@app.route("/profile")
@login_required
def profile():
  return render_template("profile.html", title="Profile", user=current_user, courses=["Test 1", "Test 2"])

@app.route("/quiz")
@login_required
def quiz():
  form = QuizQuestionForm()
  return render_template("quiz.html", title="Quiz", user=current_user, form=form)


@app.route("/logout")
@login_required
def logout():
  logout_user()
  flash('Logged out succesfully', 'success')
  return redirect(url_for('index'))

@app.errorhandler(404)
@app.route("/404")
def error404(error=404):
  return render_template("error404.html", title="Page Not Found")


@app.route("/users")
def users():
  if current_user.is_authenticated and current_user.admin:
    users = get_all_user()
    return render_template("users.html", users=users)
  else:
    return redirect(url_for('dashboard'))

@app.route("/edit-quiz/<quiz_id>" , methods=["POST","GET"])
@login_required
def edit_quiz(quiz_id):
  form = AddQuestionForm()
  quiz = Quiz.query.filter_by(id = quiz_id).first()
  
  if current_user.admin and form.validate_on_submit():
    question = Question.query.filter_by(quiz_id = quiz_id).filter_by(question=form.question.data).first()
    if question is not None:
      flash("Question already added")
    else:
      question = Question(question=form.question.data, answer=form.answer.data, quiz=quiz)
      db.session.add(question)
      db.session.commit()
  all_questions = Question.query.filter_by(quiz_id = quiz_id).all()
  if quiz is not None:
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