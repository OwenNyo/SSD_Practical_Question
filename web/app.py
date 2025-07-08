from flask import Flask, request, render_template, redirect, url_for
import re
import os

app = Flask(__name__)

def load_common_passwords():
    file_path = os.path.join(os.path.dirname(__file__), 'common_passwords.txt')
    with open(file_path) as f:
        return set(p.strip() for p in f.readlines())

COMMON_PASSWORDS = load_common_passwords()

def is_valid_password(password):
    if password in COMMON_PASSWORDS:
        return False
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*()_+=\-{}[\]:;\"'<>,.?/]", password):
        return False
    return True

@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        if is_valid_password(password):
            return redirect(url_for('welcome', password=password))
        else:
            error = "Invalid password."
    return render_template("home.html", error=error)

@app.route("/welcome")
def welcome():
    password = request.args.get("password", "")
    return render_template("welcome.html", password=password)

@app.route("/logout")
def logout():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
