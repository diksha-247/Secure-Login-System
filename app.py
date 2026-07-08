from flask import Flask, render_template, request, redirect, session
import bcrypt

app = Flask(__name__)
app.secret_key = "my_secret_key"

users = {}

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        users[username] = hashed_password

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            if bcrypt.checkpw(password.encode(), users[username]):
                session["user"] = username
                return "Login Successful"

        return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return "Logged Out Successfully"

if __name__ == "__main__":
    app.run(debug=True)
