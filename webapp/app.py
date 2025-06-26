from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired
import re
import os

app = Flask(__name__)
app.secret_key = "super-secret-key"  # Required for CSRF
app.config['WTF_CSRF_ENABLED'] = False


csrf = CSRFProtect(app)

# Password form with CSRF token
class PasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

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

@csrf.exempt
@app.route("/", methods=["GET", "POST"])
def home():
    form = PasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        if is_valid_password(password):
            return redirect(url_for('welcome', password=password))
        else:
            return render_template("home.html", form=form, error="Invalid password.")
    return render_template("home.html", form=form)

@app.route("/welcome")
def welcome():
    password = request.args.get("password", "")
    return render_template("welcome.html", password=password)

@app.route("/logout")
def logout():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
