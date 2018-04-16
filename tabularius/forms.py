from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     TextAreaField)
from wtforms.validators import (DataRequired, ValidationError, Email, EqualTo,
                                Length)
from tabularius.models import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember Me')
    submit = SubmitField('sign in')


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField(
        'verify password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('register')

    # validator methods in form of validate_<thing> are automatically pulled in
    # by wtforms and invoked them
    def validate_username(self, username):
        # should only ever be one user, ergo must check to prevent db error
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            # raise error to user
            raise ValidationError(
                'username already taken, please use a different username')

    def validate_email(self, email):
        # an email should only be used by a single user, ergo check
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            # raise error to user
            raise ValidationError(
                'email already taken, please use different email address')


class EditProfileForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    about = TextAreaField('about me', validators=[Length(min=0, max=300)])
    school = StringField('school', validators=[Length(min=0, max=120)])
    role = StringField('role', validators=[Length(min=0, max=60)])
    submit = SubmitField('submit edits')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(
                    'name already taken, please use a ' + 'different username')


class ResetPassswordRequestForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('request password reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField(
        'verify password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('request password reset')
