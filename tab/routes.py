from tab import tab_app


@tab_app.route('/')
@tab_app.route('/index')
def index():
    return "tabularius v2"
