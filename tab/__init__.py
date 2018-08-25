from flask import Flask

tab_app = Flask(__name__)

# avoids circular dependencies because python is special like that
from tab import routes
