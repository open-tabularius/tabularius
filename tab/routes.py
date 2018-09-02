from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from tab import tab_app, db
from tab.forms import LoginForm, RegistrationForm, ProfileForm
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


@tab_app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('you are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)


@tab_app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@tab_app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        #     user = User.query.filter_by(username=form.username.data).first()
        #     if user is not None:
        #         flash('username already taken, try another')
        #         return redirect(url_for('edit_profile'))
        current_user.username = form.username.data
        db.session.commit()
    elif request.method == 'GET':
        form.username.data = current_user.username
        print(current_user.email)
        form.email.data = current_user.email
        #     return render_template(
        #         'edit_profile.html', form=form, user=current_user)
    return render_template(
        'edit_profile.html', form=form, current_user=current_user)

    # print("oh no")
    # return render_template(
    #     'edit_profile.html', form=form, current_user=current_user)

    # # old shit
    # # --------------------
    # form = ProfileForm(current_user)
    # if form.validate_on_submit():
    #     pass
    # print("oh no")
    # return render_template(
    #     'edit_profile.html', form=form, current_user=current_user)
    # user = User.query.filter_by(username=form.username.data).first()
    # email = User.query.filter_by(email=form.email.data).first()


@tab_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
