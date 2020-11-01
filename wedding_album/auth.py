import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=generate_password_hash(password), role='guest')

        user = User.objects(username=username)

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif len(user) != 0:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            new_user.save()

            return redirect(url_for('auth.login'))

        flash(error, category='error')

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.objects(username=username)[0]

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()

            session['user_id'] = str(user.id)
            return redirect(url_for('index'))

        flash(error, category='error')

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.objects(id=user_id)[0]


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


def host_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user.role != 'host':
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/manage_users')
@login_required
@host_required
def manage_users():
    users = User.objects()

    return render_template('auth/manage_users.html', users=users)


@bp.route('/_change_role')
@login_required
@host_required
def change_role():
    user_id = request.args.get('id', 0, type=str)

    user = User.objects(id=user_id)[0]
    if user.role == 'host':
        user.role = 'guest'
    else:
        user.role = 'host'

    user.save()

    return jsonify(result=user.role)
