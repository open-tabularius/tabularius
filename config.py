import os

basedir = os.path.abspath(os.path.dirname(__name__))
DATABASE_URI = "postgresql://spook:tab_dev@haunt/tab_dev"


class Config():
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or "wu tang clan comin' at ya"
