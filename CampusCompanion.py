from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
import flask
import forms
from flask_wtf.csrf import CSRFProtect

import string

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
    if 'user' in flask.request.cookies:
        user = flask.request.cookies.get('user')

    #Get all the submissions in the DB
    allSubmissions = models.CCIssue.query.all()
    #Pass it to the html
    return render_template("index.html", submissions=allSubmissions)

@app.route('/mysubmissions')
def mysubs():
    if 'user' in flask.request.cookies:
        user_id = flask.request.cookies.get('user').split(" ")[1].replace(">", "")
        # Get all the submissions in the DB
        allSubmissions = models.CCIssue.query.filter(models.CCIssue.user_id == user_id).all()
        # Pass it to the html
        return render_template("mysubmissions.html", submissions=allSubmissions)
    else:
        return flask.redirect('/login', code=302)

@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    #If the users already logged in, go index
    if 'user' in flask.request.cookies:
        return flask.redirect('/', code=302)

    loginForm = forms.LoginForm()
    if loginForm.validate_on_submit():
        data = models.CCUser.query.filter_by(email=loginForm.email.data, password=loginForm.password.data).first()
        print(data)
        if data is not None:
            resp = flask.make_response(flask.redirect('/', code=302))
            resp.set_cookie('user', str(data))
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

@app.route('/map')
def map():
    return flask.render_template('map.html')
@app.route('/reportIssue', methods=['GET', 'POST'])
def reportIssue():
    if 'user' not in flask.request.cookies:
        return flask.redirect('/login', code=302)

    issueForm = forms.IssueForm()
    if issueForm.validate_on_submit():
        flask.flash('Issue reported successfully!', 'success')

        #need to check somehow if the issue has been reported
        #in which case doesnt create another row in the db..
        if False:
            return 0

        #store the issue in the db
        #TODO need to specify the user id
        else:
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            user_id = flask.request.cookies.get('user').split(" ")[1].replace(">", "")

            issue = models.CCIssue(issueForm.title.data, issueForm.description.data, issueForm.image.data,
                           issueForm.location.data, date_time, None, user_id, False)

            db.session.add(issue)
            db.session.commit()
            return flask.redirect('/', code=302)
    return flask.render_template('reportIssue.html', form=issueForm)


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
