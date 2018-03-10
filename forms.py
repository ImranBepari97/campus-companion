from flask_wtf import FlaskForm
import wtforms as fields
import wtforms.validators as validators
import wtforms.widgets as widgets

# Create a poll
class CreateLoginForm(FlaskForm):
    username = fields.StringField('title', validators=[validators.DataRequired()])
    password = fields.StringField('description', widget=widgets.TextArea(), validators=[validators.DataRequired()])
    submit = fields.SubmitField(label='Create')

# Add response to a poll
class ResponseForm(FlaskForm):
    response = fields.StringField('response', validators=[validators.DataRequired()])
    submit = fields.SubmitField(label='Add')


# Check user intends to delete poll
class DeleteForm(FlaskForm):
    submit = fields.SubmitField(label='Delete')