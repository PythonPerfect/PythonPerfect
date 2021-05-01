from flask import Flask, render_template, redirect, url_for, request, session, flash
from app import app

@app.route("/")
def index():
  if "user" in session:
    user = session["user"]
    return render_template("index.html", title="Python Perfect", user=user)
  else:
    return render_template("index.html", title="Python Perfect")


@app.route("/login", methods=["POST", "GET"])
def login():
  if request.method == "POST":
    current_user = request.form["username"] 
    session["user"] = current_user
    flash("You have been logged in successfully!", "info")

    return redirect(url_for("dashboard"))
  else:
    if "user" in session:
      flash("You are already logged in!", "info")
      return redirect(url_for("dashboard"))
    return render_template("login.html", title="Login")

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
def dashboard():
  if "user" in session:
    user = session["user"]
    return render_template("dashboard.html", title="Dashboard", user=user)
  else:
    flash("Please Log in first!", "info")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
  if "user" in session:
    user = session["user"]
    flash("You have logged out successfully!", "info")
  session.pop("user", None)
  return redirect(url_for("index"))

@app.errorhandler(404)
@app.route("/404")
def error404(e):
  return render_template("error404.html", title="Error 404")

if __name__ == "__main__":
    app.run(debug=True)