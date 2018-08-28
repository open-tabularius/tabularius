from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

tab_app = Flask(__name__)
tab_app.config.from_object(Config)

# DB stuff
db = SQLAlchemy(tab_app)
migrate = Migrate(tab_app, db)

# user login management
login = LoginManager(tab_app)
login.login_view = 'login'

# avoids circular dependencies because python is special like that
from tab import routes, models
