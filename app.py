"""This module does password validation."""
import re
import socket

from functools import wraps
from datetime import datetime
from flask import Flask, redirect, url_for, render_template, request, session, flash
from forms import LoginForm, RegisterForm, ResetPassword

webApp = Flask(__name__)

webApp.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def add_to_logs():
    with open('./failed-login.txt', 'a+') as f:
        f.write(get_date() + "\t" + get_ip() + "\n")
        f.close()


def get_date():
    """
    This function gets the current date (e.g. April 24, 2020). :return: date
    """
    today = datetime.today()
    date = today.strftime("%B %d, %Y")  # Month, day and year return date
    return date


def validate(password):
    """Validate password."""
    if len(password) < 12:
        return False
    elif re.search('[0-9]', password) is None:
        return False
    elif re.search('[A-Z]', password) is None:
        return False
    elif re.search('[a-z]', password) is None:
        return False
    elif re.search('[@_!#$%^&*()<>?/|}{~:]', password) is None:
        return False
    else:
        return True


def login_required(func):
    """Check if user is logged."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is None:
            return redirect('/login', code=302)
        return func(*args, **kwargs)
    return decorated_function


# User Registration Api End Point
@webApp.route('/register', methods=['GET', 'POST'])
def register():
    """Creating Register form object."""
    form = RegisterForm(request.form)
    # Cheking that method is post and form is valid or not.
    if request.method == 'POST' and form.validate():
        if validate(form.password.data):
            # database or file
            flash('You have successfully registered', 'success')
            # if registration successful, then redirecting to login Api
            return redirect(url_for('login'))
        else:
            flash('Password should have atleast one Lowercase, one Uppercase, one Number and  one special character', "Danger")
            return redirect(url_for('register'))
    else:
        # if method is Get, than render registration form
        return render_template('register.html', form=form)


# Login API endpoint implementation
@webApp.route('/login', methods=['GET', 'POST'])
def login():
    """Creating Login form object."""
    form = LoginForm(request.form)
    # verifying that method is post and form is valid
    if request.method == 'POST' and form.validate:
        if validate(form.password.data):
            flash('You have successfully logged in', 'success')
            print("You have successfully logged in.")
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Password not correct', "Danger")
            add_to_logs()
            return redirect(url_for('login'))
        # After successful login, redirecting to home page
    else:
        # rendering login page
        return render_template('login.html', form=form)


# User Registration Api End Point
@webApp.route('/reset-password', methods=['GET', 'POST'])
def resetPassword():
    """Reset password."""
    form = ResetPassword(request.form)
    # Cheking that method is post and form is valid or not.
    if request.method == 'POST' and form.validate():
        if validate(form.password.data):
            # database or file
            flash('You have successfully changed your password', 'success')
            return redirect(url_for('home'))
        else:
            flash('Password should have atleast one Lowercase, one Uppercase, one Number and  one special character', "Danger")
            return redirect(url_for('resetPassword'))
    else:
        return render_template('reset-password.html', form=form)


@webApp.route('/logout')
def logout():
    """Removing data from session by setting logged_flag to False."""
    session['logged_in'] = False
    # redirecting to home page
    return redirect(url_for('home'))


@webApp.route("/home")
def index():
    """Return the home page"""
    date = get_date()
    return render_template("index.html", content=[date])


@webApp.route("/")
def home():
    """Redirect to homepage."""
    return redirect((url_for("index")))


@webApp.route("/presidents")
def presidents():
    """Redirect to presidents page."""
    date = get_date()
    return render_template("presidents.html", content=[date])


@webApp.route("/info")
def info():
    """Render to info page."""
    date = get_date()
    return render_template("info.html", content=[date])


@webApp.route("/admin")
@login_required
def admin():
    """Redirect to home."""
    return redirect((url_for("index")))


if __name__ == "__main__":
    webApp.run(port=5050, debug=True)
