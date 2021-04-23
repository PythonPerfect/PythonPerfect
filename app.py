from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html", title="Python Perfect")

@app.route("/login", methods=["POST", "GET"])
def login():
  if request.method == "POST":
    current_user = request.form["username"] 
    return redirect(url_for("dashboard", user=current_user))
  else:
    return render_template("login.html", title="Login")

@app.route("/signup", methods=["POST", "GET"])
def signup():
  if request.method == "POST":
    current_user = request.form["username"] 
    return redirect(url_for("dashboard", user=current_user))
  else:
    return render_template("signup.html", title="Sign Up")

@app.route("/dashboard/<user>")
def dashboard(user):
  return render_template("dashboard.html", title="Dashboard", user=user)

@app.errorhandler(404)
@app.route("/404")
def error404(e):
  return render_template("error404.html", title="Error 404")

if __name__ == "__main__":
    app.run(debug=True)