from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
  return render_template("login.html")

@app.errorhandler(404)
@app.route("/404")
def error404(e):
  return render_template("error404.html")

if __name__ == "__main__":
    app.run()