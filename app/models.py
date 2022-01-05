from datetime import datetime

from sqlalchemy.orm import relationship

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
#    role = db.Column(db.Boolean)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    railwagon = relationship("Railwagon", back_populates="trains")
    personwagons = relationship("Personwagon", backref='train', lazy='dynamic')

    def __repr__(self):
        return '<Train {}>'.format(self.id)


class Railwagon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    max_traction = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'))

    def __repr__(self):
        return '<Railwagon {}>'.format(self.id)


class Personwagon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seats = db.Column(db.Integer, nullable=False)
    max_weight = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'))

    def __repr__(self):
        return '<Personwagon {}>'.format(self.id)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
