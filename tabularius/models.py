from tabularius import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    documents = db.relationship('Document', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


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


# class Attendance(db.
