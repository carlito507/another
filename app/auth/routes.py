from flask import render_template, redirect, url_for, request, flash, Blueprint, session, make_response
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required, UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import current_app
from datetime import datetime, timedelta

from ..models import User

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    flash('Hello World')
    users = current_app.db.users.find()
    for user in users:
        print(user)
    return render_template('index.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_in_db = current_app.db.users.find_one({'username': form.username.data})
        if user_in_db is None:
            flash('User {} not found.'.format(form.username.data))
            return redirect(url_for('auth.login'))
        if not check_password_hash(user_in_db['password'], form.password.data):
            flash('Incorrect password.')
            return redirect(url_for('auth.login'))
        user = User(form.username.data)
        login_user(user, remember=form.remember_me.data)
        token = create_access_token(identity=user.username, expires_delta=timedelta(minutes=5))
        flash('Login successful for user {}'.format(form.username.data))
        response = make_response(render_template('dashboard.html'))
        response.set_cookie('token', token)
        return response
    return render_template('login.html', title='Sign In', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        user_in_db = current_app.db.users.find_one({'username': form.username.data})
        if user_in_db is not None:
            flash('User {} already exists.'.format(form.username.data))
            return redirect(url_for('auth.register'))
        password_hash = generate_password_hash(form.password.data)
        current_app.db.users.insert_one({'username': form.username.data, 'email': email, 'password': password_hash})
        flash('Registration requested for user {}, email={}'.format(form.username.data, email))
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)


@auth.route('/logout')
def logout():
    return redirect(url_for('auth.index'))




