from datetime import datetime
from tab import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    """
    getter for flask-login to retrieve an active sessions's user id.
    """
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # relations to other tables
    # note, we reference the table as declared in models.py, aka capitalized
    documents = db.relationship('Document', backref='uploader', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
