from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from tab import tab_app
from tab.forms import LoginForm
from tab.models import User
from werkzeug.urls import url_parse


@tab_app.route('/')
@tab_app.route('/index')
@login_required
def index():
    return render_template('index.html', title='home')


@tab_app.route('/login', methods=['GET', 'POST'])
def login():
    # check if user logged in, redirect if so
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # else, authenticate as expected
    form = LoginForm()
    if form.validate_on_submit():
        # check for User existence with submitted credentials
        user = User.query.filter_by(username=form.username.data).first()

        # check if invalid input or non-existent user
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        # enable redirection of user to desired page after logging in
        next_page = request.args.get('next')

        # if not being redirected or non-relative link, just send them to index
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    # default case for not logged in user accessing login page
    return render_template('login.html', title='sign in', form=form)


@tab_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
