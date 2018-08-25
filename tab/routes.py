from flask import render_template, flash, redirect, url_for
from tab import tab_app
from tab.forms import LoginForm


@tab_app.route('/')
@tab_app.route('/index')
def index():
    user = {'username': 'spook'}
    return render_template('index.html', title='home', user=user)


@tab_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))

    return render_template('login.html', title='sign in', form=form)
