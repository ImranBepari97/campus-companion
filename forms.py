from flask_wtf import FlaskForm
import wtforms as fields
import wtforms.validators as validators

# Login form
class LoginForm(FlaskForm):
    username = fields.StringField('Username', validators=[validators.DataRequired()])
    password = fields.PasswordField('Password', [
        validators.DataRequired(),
    ])
    submit = fields.SubmitField(label='Login')

# Register form
class RegistrationForm(FlaskForm):
    username = fields.StringField('Username', [validators.Length(min=4, max=25)])
    email = fields.StringField('Email Address', [validators.Length(min=6, max=35)])
    password = fields.PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = fields.PasswordField('Repeat Password')
    submit = fields.SubmitField(label='Register')