from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler

# application is created as an instance of Flask and we pass it __name__
# in order load resources correctly for our module
app = Flask(__name__)
app.config.from_object(Config)

# database setup
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# handle logins
login = LoginManager(app)
login.login_view = 'login'

# TODO: use flask-avatars to remove dependency on gravatar
# handle avatars
# avatar = Avatar(app)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
                mail_handler = SMTPHandler(
                    mailhost=(app.config['MAIL_SERVER'],
                              app.config['MAIL_PORT']),
                    fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                    toaddrs=app.config['ADMINS'],
                    subject='tabularius failure',
                    credentials=auth,
                    secure=secure)
                mail_handler.setLevel(logging.ERROR)
                app.logger.addHandler(mail_handler)

# we place the import statement here to avoid circular imports.
from tabularius import routes, models, errors
