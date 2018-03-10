import flask
import forms
from flask import Flask, render_template, request, session, redirect, flash


app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True
)

@app.route('/')
def hello_world():
    return render_template("index.html", title="Home", page='home')


@app.route('/login', methods=['GET', 'POST'])
def create():
    form = forms.CreateLoginForm()
    if form.validate_on_submit():
        flask.flash('Poll created successfully', 'success')
    return flask.render_template('create.html', title='Submit a Complaint', form=form)

if __name__ == '__main__':
    app.run()
