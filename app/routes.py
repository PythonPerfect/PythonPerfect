from flask import Flask, render_template, redirect, url_for, request, session, flash
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddCourseForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Course
from werkzeug.urls import url_parse

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
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()

    login_user(user, remember=False)
    flash('Welcome, registration complete!')
    return redirect(url_for('dashboard'))
  return render_template('signup.html', title='Signup', form=form)

mock_course_data = [
  "Course A",
  "Course B",
  "Course C",
  "Course D",
  "Course E",
  "Course F",
  "Course G",
  "Course H",
    "Course A",
  "Course B",
  "Course C",
  "Course D",
  "Course E",
  "Course F",
  "Course G",
  "Course H",
    "Course A",
  "Course B",
  "Course C",
  "Course D",
  "Course E",
  "Course F",
  "Course G",
  "Course H",
    "Course A",
  "Course B",
  "Course C",
  "Course D",
  "Course E",
  "Course F",
  "Course G",
  "Course H",
    "Course A",
  "Course B",
  "Course C",
  "Course D",
  "Course E",
  "Course F",
  "Course G",
  "Course H",
]

@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
  form = AddCourseForm()
  if form.validate_on_submit():
    new_course = Course(title=form.title.data)
    course = Course.query.filter_by(title = form.title.data).first()

    if course is None:
      db.session.add(new_course)
      db.session.commit()
  else:
    flash("Course already added. Please add another course.")
  # if form.validate_on_submit():
  #   course = Course(title=form.title.data)
  #   db.session.add(course)
  #   db.session.commit()

  all_courses = Course.query.all()
  return render_template("dashboard.html", title="Dashboard", form=form, courses=all_courses)

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.errorhandler(404)
@app.route("/404")
def error404(e):
  return render_template("error404.html", title="Error 404")


@app.route("/users")
def users():
  users = User.query.all()
  return render_template("users.html", users=users)

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

if __name__ == "__main__":
    app.run(debug=True)