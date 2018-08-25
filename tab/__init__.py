from flask import Flask
from config import Config

tab_app = Flask(__name__)
tab_app.config.from_object(Config)

# avoids circular dependencies because python is special like that
from tab import routes
