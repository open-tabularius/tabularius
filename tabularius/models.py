from tabularius import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


# methods necessary for flask_login to work
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    documents = db.relationship('Document', backref='author', lazy='dynamic')
    about = db.Column(db.String(300))
    school = db.Column(db.String(120))
    role = db.Column(db.String(60))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        # TODO: use flask-avatar instead of relying on stupid gravatar
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upload_name = db.Column(db.String(64), index=True)
    file_name = db.Column(db.String(64), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    file = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<File {}>'.format(self.upload_name)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssn_id = db.Column(db.Integer, index=True, unique=True)
    ps_id = db.Column(db.Integer, index=True, unique=True)
    local_id = db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
        return '<Student {}>'.format(self.ssn_id)
