from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    devices = db.relationship('Device', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(128), index=True, default='location')
    battery_percentage = db.Column(db.Integer, default=100)
    food_percentage = db.Column(db.Integer,default=100)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cats = db.relationship('Cat',backref='kitchen', lazy='dynamic')

    def set_location(self, location):
        self.location = location

    def set_battery(self, battery):
        self.battery_percentage = battery

    def set_food_level(self, food_level):
        self.food_percentage = food_level

    def __repr__(self):
        return '<Device {}>'.format(self.location)

class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, default='name')
    last_feeding_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

    def set_name(self, name):
        self.name = name

    def __repr__(self):
        return '<Cat {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
