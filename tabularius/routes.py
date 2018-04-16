from tabularius import app, db
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from tabularius.forms import (LoginForm, RegistrationForm, EditProfileForm,
                              ResetPassswordRequestForm, ResetPasswordForm)
from tabularius.models import User
from tabularius.email import send_password_reset_email, send_email
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    # mock posts
    posts = [{
        'author': {
            'username': 'elias julian marko garcia'
        },
        'body':
        'tabularius is a comprehensive platform for educators to help ' +
        'their students succeed.'
    }, {
        'author': {
            'username': 'xenophon'
        },
        'body':
        'if you consider what are called the virtues in mankind,' +
        ' you will find their growth is assisted by education and cultivation.'
    }]
    return render_template('index.html', title='home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # no point logging in if you are already logged in
    if current_user.is_authenticated:
        # TODO popup saying "you are already logged in, fam"
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # filter user database and see if they exist && used correct password
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            # failed to login, try again
            flash('invalid username or password.')
            return redirect(url_for('login'))

        # login user
        login_user(user, remember=form.remember_me.data)

        # attempt to pull rediret information from url
        next_page = request.args.get('next')

        # if login not inbound from redirect, set default next page to index
        # and prevent url injection
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        # redirect successful login to original destination
        return redirect(next_page)
    # failed to validate, retry
    return render_template('login.html', title='Sign in', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    # if successful, add them into the system.
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        # add new user to dbs
        # TODO prevent registration abuse
        db.session.add(user)
        db.session.commit()
        flash('you have succesfully registered for tabularius!')
        return redirect(url_for('login'))
    # retry registration
    return render_template('register.html', title='register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    # TODO: use flask-avatar instead of gravitar for avatar in models.py
    user = User.query.filter_by(username=username).first_or_404()
    posts = [{
        'author': user,
        'body': 'another post on tabularius!'
    }, {
        'author': user,
        'body': 'my first post on tabularius! hooray!'
    }]

    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    # work that needs to be done before a view executes can go here
    pass


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        # get all form updates
        current_user.username = form.username.data
        current_user.role = form.role.data
        current_user.school = form.school.data
        current_user.about = form.about.data

        # commit updates to user entry in dbs
        db.session.commit()

        flash('profile changes saved')
        return redirect(url_for('edit_profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.role.data = current_user.role
        form.school.data = current_user.school
        form.about.data = current_user.about

    return render_template(
        'edit_profile.html', title='edit profile', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPassswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('check your email for a password reset link')
        return redirect(url_for('login'))

    return render_template(
        'reset_password_request.html', title='reset password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
