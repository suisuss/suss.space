from flaskapp import db
from datetime import datetime
from flaskapp.admin.models import User


class Messages(db.Model):
    __tablename__ = 'message'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(10), nullable=True)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Message('{self.id}' , '{self.name}', '{self.email}', '{self.message}', '{self.date_submitted}')"


class Post(db.Model):
    __tablename__ = 'post'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class PArticle(db.Model):
    __tablename__ = 'particle'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tags = db.Column(db.String(100), nullable=False)
    overview = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=True)
    thumbnail = db.Column(db.String(20), nullable=False)
    html_filename = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship(User)

    def __repr__(self):
        return f"Programming Article('{self.id}' , '{self.title}', '{self.date_posted}')"
