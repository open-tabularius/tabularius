from flask import render_template
from tab import tab_app
from tab.forms import LoginForm


@tab_app.route('/')
@tab_app.route('/index')
def index():
    user = {'username': 'spook'}
    return render_template('index.html', title='home', user=user)


@tab_app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='sign in', form=form)
