from flask_wtf import FlaskForm
import wtforms as fields
import wtforms.validators as validators

# Login form
class LoginForm(FlaskForm):
    email = fields.StringField('Username', validators=[validators.DataRequired()])
    password = fields.PasswordField('Password', [
        validators.DataRequired(),
    ])
    submit = fields.SubmitField(label='Login')

# Register form
class RegistrationForm(FlaskForm):
    email = fields.StringField('Email Address', [validators.Length(min=6, max=35)])
    password = fields.PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = fields.PasswordField('Repeat Password')
    submit = fields.SubmitField(label='Register')


# Issue report
class IssueForm(FlaskForm):
    title = fields.StringField('Title', [validators.DataRequired()])
    description = fields.TextAreaField('Description', [validators.DataRequired(), validators.length(max=500)])
    location = fields.StringField('Location', [validators.DataRequired()])
    image = fields.StringField('Image URL')
    submit = fields.SubmitField(label='Submit')