from flask import Flask, render_template, redirect, url_for, request, session, flash
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
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
      page_next = url_for('index')
    return redirect(page_next)
  return render_template('login.html', title='Sign In', form=form)

@app.route("/signup", methods=["POST", "GET"])
def signup():
  if request.method == "POST":
    current_user = request.form["username"] 
    session["user"] = current_user
    flash("You have signed in successfully!", "info")
    return redirect(url_for("dashboard"))
  else:
    if "user" in session:
      return redirect(url_for("dashboard"))
    return render_template("signup.html", title="Sign Up")

@app.route("/dashboard")
@login_required
def dashboard():
  return render_template("dashboard.html", title="Dashboard")

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.errorhandler(404)
@app.route("/404")
def error404(e):
  return render_template("error404.html", title="Error 404")

if __name__ == "__main__":
    app.run(debug=True)