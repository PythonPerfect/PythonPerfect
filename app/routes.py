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

  print(get_all_question_response())
  #delete_all_question_response()
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
    return render_template("course.html", course=course, title=course.title, form_content=form_content, form_quiz=form_quiz, all_content=all_content, all_quiz = all_quiz, get_user_content_viewed = get_user_content_viewed)
  else:
    return redirect(url_for('error404'))

@app.route("/course/content/add/<course_id>", methods=["POST", "GET"])
def add_content(course_id):
  form = AddContentForm()
  course = get_course_by_id(course_id)
  if form.validate_on_submit():
    content = get_content_by_course_n_title(course, form.title.data)
    if content is not None:
      flash("Content already added.", 'info')
    else:
      default_text = "<h1>" + form.title.data + "</h1>"
      add_new_content(form.title.data, default_text, course)
  return redirect(url_for('course', course_id = course_id))

@app.route("/course/quiz/add/<course_id>", methods=["POST", "GET"])
def add_quiz(course_id):
  form = AddQuizForm()
  course = get_course_by_id(course_id)
  if form.validate_on_submit():
    quiz = get_quiz_by_course_n_title(course, form.title.data)
    if quiz is not None:
      flash("Quiz already added.", 'info')
    else:
      add_new_quiz(form.title.data, course)
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
  add_new_content_viewed(viewed=True, user=current_user, content=content)

  return render_template("view-content.html", content=content, title=content.title)
# -----------------------------------------------------------------------------

# Quiz Edit related routes
# -----------------------------------------------------------------------------
@app.route("/quiz/edit/<quiz_id>" , methods=["POST","GET"])
@login_required
def edit_quiz(quiz_id):
  form = AddQuestionForm()
  quiz = get_quiz_by_id(quiz_id)
  
  if current_user.admin and form.validate_on_submit():
    question = get_question_by_quiz_n_question(quiz, form.question.data)
    if question is not None:
      flash("Question already added", "info")
    else:
      add_new_question(form.question.data, form.answer.data, quiz)
  all_questions = get_questions_by_quiz(quiz)
  if quiz is not None:
    return render_template("edit-quiz.html", form=form, questions = all_questions, quiz=quiz)
  else:
    return redirect(url_for('error404'))
# -----------------------------------------------------------------------------

# Quiz Running related routes
# -----------------------------------------------------------------------------
current_question_index = 0
current_question_id = 0
@app.route("/quiz/<quiz_id>", methods=["POST", "GET"])
@login_required
def quiz(quiz_id):
  global current_question_index
  global current_question_id
  current_question_index = 0
  current_question_id = 0


  form = QuizQuestionForm()
  quiz = get_quiz_by_id(quiz_id)
  questions = get_questions_by_quiz(quiz)

  session["quiz"] = [q.id for q in questions]
  if len(session["quiz"]):
    current_question_id = int(session["quiz"][0])
  
  question = get_question_by_id(current_question_id)

  return render_template("quiz.html", title="Quiz", user=current_user, form=form, question=question, quiz=quiz)

@app.route("/quiz/attempt/<quiz_id>", methods=["POST", "GET"])
@login_required
def next_question(quiz_id):
  global current_question_index
  global current_question_id
  last = False
  form = QuizQuestionForm()
  quiz = get_quiz_by_id(quiz_id)
  question = get_question_by_id(current_question_id)
  if form.validate_on_submit():
    session[str(current_question_id)] = form.answer.data
    quiz = session["quiz"]
    current_question_index += 1

    current_question_id = int(session["quiz"][current_question_index])
    question = get_question_by_id(current_question_id)
    if current_question_index + 1 >= len(session["quiz"]):
      last = True
  
  return render_template("quiz.html", title="Quiz", quiz=quiz, user=current_user, form=form, question=question, last=last)


@app.route("/quiz/submit", methods=["POST", "GET"])
@login_required
def submit_quiz():
  form = QuizQuestionForm()
  if form.validate_on_submit():
    session[str(current_question_id)] = form.answer.data
    added = False
    
    for id in session["quiz"]:
      if str(id) in session:
        response = session[str(id)]
        question = get_question_by_id(int(id))
        quiz = get_quiz_by_id(question.quiz_id)
        correct = question.answer == response
        if not added:
          result = add_new_result(current_user, quiz)
          added = True
        question_response = add_new_question_response(response, question, current_user, correct, result)

  
  
    for id in session["quiz"]:
      if str(id) in session:
        del session[str(id)]
    flash("Congrats, you have submitted your quiz. Check your results in the profile page", "info")
    return redirect(url_for("index"))
  return render_template("quiz.html", title="Quiz", quiz=quiz, user=current_user, form=form, question=question, last=last)




# -----------------------------------------------------------------------------

# Profile
@app.route("/profile")
@login_required
def profile():
  all_results = get_all_results()
  return render_template("profile.html", title="Profile", user=current_user, all_results=all_results)

# Users
@app.route("/users")
@login_required
def users():
  if current_user.admin:
    
    users = get_nonadmins()
    admins = get_admins()

    return render_template("users.html", users=users, admins=admins)
  else:
    return redirect(url_for('dashboard'))


# Delete related routes
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

if __name__ == "__main__":
    app.run(debug=True)