import os


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or "wu tang clan comin' at ya"
