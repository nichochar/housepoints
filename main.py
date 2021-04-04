import logging

from flask import current_app, flash, Flask, Markup, redirect, render_template, session
from flask import request, url_for
from flask_login import LoginManager, login_user, login_required
import google.cloud.logging

import db
from user import User
try:
    from secret import SECRET_KEY
    secret_key = SECRET_KEY
except ImportError:
    # If you haven't yet, you should create a local secret.py
    # file with SECRET_KEY = "your secret key" in it. This file
    # is ignored by .git for security purposes
    secret_key = "temp key"


app = Flask(__name__)
app.config.update(
    SECRET_KEY=secret_key,
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif'])
)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


# Configure logging
if not app.testing:
    logging.basicConfig(level=logging.INFO)
    client = google.cloud.logging.Client()
    # Attaches a Google Stackdriver logging handler to the root logger
    client.setup_logging()


DB = db.get_db(app.debug)


@app.route('/')
def points():
    houses = DB.get_houses()
    houses_dict = {house['name']: house for house in houses}
    return render_template('base.html', houses=houses_dict)


@app.route('/headmaster', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        house = DB.update_house(data["house"], int(data["points"]))
        log_entry = DB.log_entry(
            data['house'],
            data['points'],
            house['points'],
            data['reason']
        )

        return redirect('/ledger')

    return render_template('form.html')


@app.route('/ledger', methods=['GET'])
def logs():
    entries = DB.get_entries()
    return render_template('ledger.html', entries=entries)


# User management
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Login and validate the user.
        # User should be of a class that is described here:
        # https://flask-login.readthedocs.io/en/latest/
        user = DB.login_and_validate_user(username, password)
        if user is None:
            flash('incorrect username/password')
            return redirect(url_for('login'))

        login_user(user)
        flash('logged in successfully')
        session['username'] = username

        next = request.args.get('next')

        return redirect(next or url_for('points'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('points'))


@login_manager.user_loader
def load_user(user_id):
    if session.get('username') == user_id:
        return User(user_id, is_authenticated=True)
    return None


@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
