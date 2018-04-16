# only import needed rn is app, rest unused because make_shell_context is fud.
from tabularius import app, db
from tabularius.models import User


# does not work but interesting idea nonetheless to hope for later
@app.shell_context_processor
def make_shell_context():
    return {
        'app': app,
        'db': db,
        'User': User,
    }
