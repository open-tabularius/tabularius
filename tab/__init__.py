from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from raven.contrib.flask import Sentry

tab_app = Flask(__name__)
tab_app.config.from_object(Config)

# DB stuff
db = SQLAlchemy(tab_app)
migrate = Migrate(tab_app, db)

# user login management
login = LoginManager(tab_app)
login.login_view = 'login'

# error management with sentry

sentry = Sentry(
    tab_app,
    dsn=
    'https://032da9b870984f59bff6e791acedb389:d885a2b4902e430e984da71df055145b@sentry.io/1272916'
)

# avoids circular dependencies because python is special like that
from tab import routes, models, errors
