from flaskapp import db
from datetime import datetime


class Message(db.Model):
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
