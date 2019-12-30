from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskapp.admin.models import User


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=2)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=2)])
    tags = StringField('Tags', validators=[DataRequired(), Length(max=100)])
    date_posted = DateField('Date')
    submit = SubmitField('Post')


class PArticleForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=2)])
    date_posted = DateField('Date')
    tags = StringField('Tags', validators=[DataRequired(), Length(max=100)])
    overview = TextAreaField('Overview', validators=[DataRequired(), Length(min=2)])
    category = StringField('Category', validators=[DataRequired(), Length(max=100)])
    thumbnail = StringField('Thumbnail', validators=[DataRequired(), Length(max=100)])
    html = StringField('HTML', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Submit')


class WArticleForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=2)])
    date_posted = DateField('Date')
    tags = StringField('Tags', validators=[DataRequired(), Length(max=100)])
    overview = TextAreaField('Overview', validators=[DataRequired(), Length(min=2)])
    category = StringField('Category', validators=[DataRequired(), Length(max=100)])
    thumbnail = FileField('Thumbnail', validators=[FileAllowed(['jpg', 'png'])])
    html = FileField('Html', validators=[FileAllowed('html')])
    css = FileField('Css', validators=[FileAllowed('css')])
    submit = SubmitField('Submit')


class MessageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(
        min=2, max=20)], render_kw={"placeholder": "Name"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    phone = StringField('Phone', render_kw={"placeholder": "Phone"})
    body = TextAreaField('Message', validators=[
        DataRequired()], render_kw={"placeholder": "Message"})
    submit = SubmitField('Send Message')


class UploadForm(FlaskForm):
    file = FileField('File', validators=[FileAllowed(['jpg', 'png'])])
    path = StringField('Path', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Submit')
