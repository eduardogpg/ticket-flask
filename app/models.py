from . import db
import datetime
from werkzeug.security import generate_password_hash


class User(db.Model):
    __tablename__ = 'users' 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(255))
    email = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def set_password(self, password):
        self.password = generate_password_hash(password)


    def __repr__(self):
        return f"<User {self.username}>"


class Event(db.Model):
    __tablename__ = 'events' 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    web_page = db.Column(db.String(255))
    address = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    user = db.relationship('User', backref=db.backref('user', lazy=True))
    
    def __repr__(self):
        return f"<Event {self.title}>"
    

class Ticket(db.Model):
    __tablename__ = 'tickets' 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    user = db.relationship('User', backref=db.backref('tickets', lazy=True))
    event = db.relationship('Event', backref=db.backref('tickets', lazy=True))
    
    def __repr__(self):
        return f"<Ticket {self.title}>"