from flask import render_template
from tab import tab_app


@tab_app.route('/')
@tab_app.route('/index')
def index():
    user = {'username': 'spook'}
    return render_template('index.html', title='home', user=user)
