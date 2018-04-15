from tabularius import app
from flask import render_template, flash, redirect, url_for
from tabularius.forms import LoginForm
from tabularius.models import User
from flask_login import current_user, login_user, logout_user


@app.route('/')
@app.route('/index')
def index():
    # mock user object
    user = {'username': 'Xenophon'}
    posts = [{
        'author': {
            'username': 'elias julian marko garcia'
        },
        'body':
        'tabularius is a comprehensive data framework for educators to help ' +
        'their students succeed.'
    }, {
        'author': {
            'username': 'Xenophon'
        },
        'body':
        'If you consider what are called the virtues in mankind,' +
        ' you will find their growth is assisted by education and cultivation.'
    }]
    return render_template('index.html', title='', user=user, posts=posts)


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
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        # succeeded
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    # failed to validate, retry
    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
