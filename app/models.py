from datetime import datetime

from sqlalchemy.orm import relationship

from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class TrainSchema(ma.Schema):
    class Meta:
        fields = ('id', 'width')


train_schema = TrainSchema()
trains_schema = TrainSchema(many=True)


class MaintenanceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'train_id', 'time')


maintenance_schema = MaintenanceSchema()
maintenances_schema = MaintenanceSchema(many=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(120), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    maintenances = db.relationship('Maintenance', cascade='all,delete', backref='worker', lazy='dynamic')

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
    width = db.Column(db.Integer, nullable=False)
    railwagon_id = db.Column(db.Integer, db.ForeignKey('railwagon.id'))
    personwagons = db.relationship('Personwagon', cascade='all,delete', backref='train', lazy='dynamic')
    maintenances = db.relationship('Maintenance', backref='train', lazy='dynamic')

    def __repr__(self):
        return '<Train {}>'.format(self.id)


class Railwagon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    max_traction = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    train_rw = db.relationship('Train', cascade='all,delete', backref='railwagon', uselist=False)

    def __repr__(self):
        return '<Railwagon {}>'.format(self.id)


class Personwagon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seats = db.Column(db.Integer, nullable=False)
    max_weight = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    train_id_pw = db.Column(db.Integer, db.ForeignKey('train.id'))

    def __repr__(self):
        return '<Personwagon {}>'.format(self.id)


class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'))
    time = db.Column(db.DateTime, index=True)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
