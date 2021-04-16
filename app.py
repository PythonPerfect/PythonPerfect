from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html", title="Python Perfect")

@app.route("/login")
def login():
  return render_template("login.html", title="Login")

@app.route("/signup")
def signup():
  return render_template("signup.html", title="Sign Up")

@app.errorhandler(404)
@app.route("/404")
def error404(e):
  return render_template("error404.html", title="Error 404")

if __name__ == "__main__":
    app.run()