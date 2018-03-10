from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
import flask
import forms


app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True
)
POSTGRES = {
    'user': 'campus',
    'pw': 'companion',
    'db': 'cc',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)


import models
db.create_all()


@app.route('/')
def hello_world():
    #now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    #u = models.CCUser('abc123@soton.ac.uk', 'password');
    #i = models.CCIssue('issue1', 'descript', 'image', 'highfiled', now, now, u.id, 0)
    #db.session.add(u)
    #db.session.add(i)
    #db.session.commit()
    return render_template("index.html", title="Home", page='home')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        flask.flash('Login successful!', 'success')
        return flask.redirect('/', code=302)
    return flask.render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    db.create_all()
    app.run()

# Error Handlers

@app.errorhandler(400)
def error_400(error):
    return flask.render_template('error.html', title='400', heading='Error 400', text="Oh no, that's an error!"), 400


@app.errorhandler(401)
def error_401(error):
    return flask.render_template('error.html', title='401', heading='Error 401', text="Oh no, that's an error!"), 401


@app.errorhandler(403)
def error_403(error):
    return flask.render_template('error.html', title='403', heading='Error 403', text="Oh no, that's an error!"), 403


@app.errorhandler(404)
def error_404(error):
    return flask.render_template('error.html', title='404', heading='Error 404', text="This page does not exist."), 404


@app.errorhandler(405)
def error_405(error):
    return flask.render_template('error.html', title='405', heading='Error 405', text="Oh no, that's an error!"), 405


@app.errorhandler(500)
def error_500(error):
    return flask.render_template('error.html', title='500', heading='Error 500', text="Oh no, that's an error!"), 500