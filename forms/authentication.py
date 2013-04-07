from wtforms import Form, BooleanField, TextField, PasswordField, validators


class SignInForm(Form):
    username = TextField('Email or Username', [
        validators.Required(),
        validators.Length(min=4, max=25)
    ])
    password = PasswordField('Password', [
        validators.Required(),
        validators.Length(min=6, max=20)
    ])
    remember = BooleanField('Remember me')


class SignUpForm(Form):
    username = TextField('Username', [
        validators.Required(),
        validators.Length(min=4, max=25)
    ])
    email = TextField('Email Address', [
        validators.Required(),
        validators.Length(min=6, max=35)
    ])
    password = PasswordField('Password', [
        validators.Required(),
        validators.Length(min=6, max=20),
    ])
