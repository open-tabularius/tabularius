from datetime import datetime
from tab import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # relations to other tables
    # note, we reference the table as declared in models.py, aka capitalized
    documents = db.relationship('Document', backref='uploader', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(120), index=True)

    # will evaluate the time function passed to it, i chose utcnow
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # map foreign key
    # note, we use naming conventions used by sqlalchemy, aka lowercase
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# TODO:
# create models for:
# - [ ] students
# - [ ] teachers
# - [ ] schools
