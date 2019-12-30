from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


class MessageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(
        min=2, max=20)], render_kw={"placeholder": "Name"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    phone = StringField('Phone', render_kw={"placeholder": "Phone"})
    body = TextAreaField('Message', validators=[
        DataRequired()], render_kw={"placeholder": "Message"})
    submit = SubmitField('Send Message')
