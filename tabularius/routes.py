from tabularius import app, db
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from tabularius.forms import LoginForm, RegistrationForm
from tabularius.models import User
from flask_login import current_user, login_user, logout_user, login_required


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
        'tabularius is a comprehensive data framework for educators to help ' +
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
