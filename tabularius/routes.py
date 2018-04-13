from tabularius import app
from flask import render_template, flash, redirect, url_for
from tabularius.forms import LoginForm


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
    form = LoginForm()
    if form.validate_on_submit():
        flash('login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)
