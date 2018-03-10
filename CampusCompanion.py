import flask
import forms
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return flask.render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def create():
    form = forms.CreateLoginForm()
    if form.validate_on_submit():
        flask.flash('Poll created successfully', 'success')
    return flask.render_template('create.html', title='Submit a Complaint', form=form)

if __name__ == '__main__':
    app.run()
