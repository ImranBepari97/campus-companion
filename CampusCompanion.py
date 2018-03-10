import flask
import forms
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return flask.render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        flask.flash('Login successful!', 'success')
        return flask.redirect('/', code=302)
    return flask.render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
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