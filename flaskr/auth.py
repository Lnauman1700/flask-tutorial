import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# creates a blueprint called auth, w/ params __name__ (current directory), url_prefix (which is just prepended to all the URLS in question)
bp = Blueprint('auth', __name__, url_prefix = '/auth')

# templates to generate an HTML form

# associates the register directory with the register function. when it gets a request to /auth/register, it'll call the register() function
# when a user inputs something, it's labeled as 'POST'
@bp.route('/register', methods = ('GET', 'POST'))
def register():
    # begin validating input
    if request.method == 'POST':
        # request.form is a dict mapping submitted form keys/values
        username = request.form['username']
        password = request.form['password']
        # assigns database to a variable
        db = get_db()
        error = None

        # if username/password fields aren't filled out, then you can't do anything
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        # runs query to see if username is present in DB
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."
        # if no similar username already exists, enter username and hashed password to DB
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            # redirects you to the given url (url_for() generates a url for the given filepath)
            return redirect(url_for('auth.login'))

        # stores the error message
        flash(error)

    return render_template('auth/register.html')

# function that gets called when a user logs in
@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        # user input
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # fetches the row where username = the user's input
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # if a user didn't enter a username or if their password hash is wrong, throw an error
        if user is None:
            error = 'Incorrect Username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect Password'

        if error is None:
            session.clear()
            # when validation succeeds, store the user's id in the dictionary session.
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
# checks if a user id is stored in teh session and gets the user's data, storing it in g.user. if your session is still running, no need to log in.
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# removes the user id from the session
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# this is a decorator
#
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
