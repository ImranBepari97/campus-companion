from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
import flask
import forms
from flask_wtf.csrf import CSRFProtect
import models

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True
)

app.secret_key = '5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e'
csrf = CSRFProtect(app)

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



db.create_all()


@app.route('/')
def hello_world():
    #now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    #u = models.CCUser('abc123@soton.ac.uk', 'password');
    #i = models.CCIssue('issue1', 'descript', 'image', 'highfiled', now, now, u.id, 0)
    #db.session.add(u)
    #db.session.add(i)
    #db.session.commit()
    if 'user' in flask.request.cookies:
        user = flask.request.cookies.get('user')
    return render_template("index.html", title="Home", page='home')



@app.route('/login', methods=['GET', 'POST'])
def login():
    #If the users already logged in, go index
    if 'user' in flask.request.cookies:
        return flask.redirect('/', code=302)

    loginForm = forms.LoginForm()
    if loginForm.validate_on_submit():
        data = models.CCUser.query.filter_by(email=loginForm.email.data, password=loginForm.password.data).first()
        if data is not None:
            resp = flask.make_response(flask.redirect('/', code=302))
            resp.set_cookie('user', data)
            flask.flash('Login successful!', 'success')
            return resp
        return flask.render_template('login.html', form=loginForm)
    return flask.render_template('login.html', form=loginForm)

@app.route('/register', methods=['GET', 'POST'])
def register():
    loginForm = forms.RegistrationForm()
    if loginForm.validate_on_submit():
        flask.flash('Registration successful!', 'success')
        #Take the information submitted, add and save the db
        if models.CCUser.query.filter_by(email=loginForm.email.data).first():
            flask.flash('User already exists!', 'warning')
            return flask.render_template('registration.html', form=loginForm)
        else:
            u = models.CCUser(loginForm.email.data, loginForm.password.data)
            db.session.add(u)
            db.session.commit()
            return flask.redirect('/', code=302)
    return flask.render_template('registration.html', form=loginForm)

@app.route('/signout')
def signout():
    if 'user' in flask.request.cookies:
        resp = flask.make_response(flask.redirect('/', code=302))
        resp.set_cookie('user', '', expires=0)
    return flask.redirect('/', code=302)

if __name__ == '__main__':
#    db.create_all()
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