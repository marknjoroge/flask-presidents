"""Forms Class"""
from wtforms import Form, StringField, PasswordField, validators


def checkIfCommon(form, password):
    with open("./commonpasswords.txt") as file:
        for line in file:
            line = line.strip()
            passw = password.data
            if line == passw:
                raise validators.ValidationError('The password you typed is common or has'
                                             ' been compromised thus unsecure. Please choose'
                                             ' another password that is unique to you'
                                             ' and easy to remember.')
                

class LoginForm(Form):
    """Creating Login Form contains email and password"""
    email = StringField("Email", validators=[
        validators.Length(min=7, max=50),
        validators.DataRequired(message="Please Fill This Field")
    ])
    password = PasswordField("Password", validators=[
        validators.Length(min=12),
        validators.DataRequired(message="Please Fill This Field"),
    ])


class ResetPassword(Form):
    """Creating Login Form contains email and password"""
    oldPassword = PasswordField("Old Password", validators=[
        validators.DataRequired(message="Please Fill This Field"),
    ])
    password = PasswordField("New Password", validators=[
        validators.Length(min=12),
        checkIfCommon,
        validators.DataRequired(message="Please Fill This Field"),
        validators.EqualTo(fieldname="confirm",
                           message="Your Passwords Do Not Match"),
    ])
    confirm = PasswordField("Confirm New Password", validators=[
        validators.Length(min=12),
        validators.DataRequired(message="Please Fill This Field")])


class RegisterForm(Form):
    """Creating Registration Form contains username, name, email, password and confirm password."""
    name = StringField("Full Name", validators=[
        validators.Length(min=3, max=25),
        validators.DataRequired(message="Please Fill This Field")
    ])
    username = StringField("Username", validators=[
        validators.Length(min=3, max=25),
        validators.DataRequired(message="Please Fill This Field")
    ])
    email = StringField("Email", validators=[
        validators.Email(message="Please enter a valid email address")
    ])
    password = PasswordField("Password", validators=[
        validators.Length(min=12),
        checkIfCommon,
        validators.DataRequired(message="Please Fill This Field"),
        validators.EqualTo(fieldname="confirm",
                           message="Your Passwords Do Not Match"),
    ])
    confirm = PasswordField("Confirm Password", validators=[
        validators.Length(min=12),
        validators.DataRequired(message="Please Fill This Field")])
