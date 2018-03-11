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
    locationBulding = fields.SelectField('locationBulding', [validators.DataRequired()], choices=[('1', '1'), ('16', '16'), ('18', '18'), ('2', '2'), ('20', '20'), ('25', '25'), ('32', '32'), ('34', '34'), ('36', '36'), ('38', '38'), ('39', '39'), ('40', '40'), ('42', '42'), ('44', '44'), ('45', '45'), ('46', '46'), ('48', '48'), ('5', '5'), ('50', '50'), ('52', '52'), ('53', '53'), ('54', '54'), ('57', '57'), ('58', '58'), ('59', '59'), ('67', '67'), ('7', '7'), ('8', '8'), ('85', '85')])
    location = fields.StringField('Location', [validators.DataRequired()])
    image = fields.StringField('Image URL')
    submit = fields.SubmitField(label='Submit')
