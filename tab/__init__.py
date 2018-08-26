from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

tab_app = Flask(__name__)
tab_app.config.from_object(Config)

# DB stuff
db = SQLAlchemy(tab_app)
migrate = Migrate(tab_app, db)

# avoids circular dependencies because python is special like that
from tab import routes, models
