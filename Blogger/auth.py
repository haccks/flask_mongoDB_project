import json, functools
from flask import (Blueprint, request, redirect, url_for, flash,
                   render_template, session, g)
from Blogger.db import get_db_client
from werkzeug.security import check_password_hash, generate_password_hash
from bson.json_util import loads, dumps, ObjectId

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        blog_db = get_db_client().blogger
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif blog_db.users.find_one({'username': username}) is not None:
            error = 'User {} already registered .'.format(username)

        if error is None:
            blog_db.users.insert_one(
                {
                    'username': username,
                    'password': generate_password_hash(password)
                }
            )
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        blog_db = get_db_client().blogger
        error = None

        user = json.loads(dumps(blog_db.users.find_one({'username': username})))

        if user is None:
            error = 'Incorrect user name.'
        elif not check_password_hash(user.get('password'), password):
            error = 'Incorrect user password.'

        if error is None:
            session.clear()
            session['user_id'] = user['_id']['$oid']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        blog_db = get_db_client().blogger
        g.user = blog_db.users.find_one({'_id': ObjectId(user_id)})
        # print(g.user)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
