import os


class Config():
    SECRET = os.environ.get('SECRET') or "wu tang clan comin' at ya"
