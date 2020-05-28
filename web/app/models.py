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
        db.session.add(self)
        db.session.commit()

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
    is_charging = db.Column(db.Boolean, default = False)
    is_on = db.Column(db.Boolean, default = False)
    turn_on  = db.Column(db.String(32), default='10:00 PM')
    turn_off = db.Column(db.String(32), default='07:00 AM')
    last_refill_time = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    cats = db.relationship('Cat',backref='kitchen', lazy='dynamic')

    def set_location(self, location):
        self.location = location
        db.session.add(self)
        db.session.commit()

    def set_battery(self, battery):
        self.battery_percentage = battery
        db.session.add(self)
        db.session.commit()

    def set_food_level(self, food_level):
        self.food_percentage = food_level
        db.session.add(self)
        db.session.commit()

    def set_turn_on(self, turn_on):
        self.turn_on = turn_on
        db.session.add(self)
        db.session.commit()

    def set_turn_off(self, turn_off):
        self.turn_off = turn_off
        db.session.add(self)
        db.session.commit()

    def toggle_charging(self):
        self.is_charging = not self.is_charging
        db.session.add(self)
        db.session.commit()

    def toggle_on_off(self):
        self.is_on = not self.is_on
        db.session.add(self)
        db.session.commit()

    def update_last_refill_time(self):
        self.last_refill_time = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def get_time_after_last_refill(self):
        diff = datetime.utcnow() - self.last_refill_time
        if diff.days != 0:
            return str(diff.days) + ' day(s) ago'
        elif diff.seconds > 3600:
            return str(diff.seconds // 3600) + ' hour(s) ago'
        elif diff.seconds > 60:
            return str(diff.seconds // 60) + ' minute(s) ago'
        else:
            return str(diff.seconds) + ' second(s) ago'

    def __repr__(self):
        return '<Device {}>'.format(self.location)

class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, default='name')
    last_feeding_time = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    feeding_amount = db.Column(db.Integer, default = 1)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

    def set_name(self, name):
        self.name = name
        db.session.add(self)
        db.session.commit()

    def set_food_amount(self, food_amount):
        self.feeding_amount = food_amount
        db.session.add(self)
        db.session.commit()

    def get_time_after_last_feeding(self):
        diff = datetime.utcnow() - self.last_feeding_time
        if diff.days != 0:
            return str(diff.days) + ' day(s) ago'
        elif diff.seconds > 3600:
            return str(diff.seconds // 3600) + ' hour(s) ago'
        elif diff.seconds > 60:
            return str(diff.seconds // 60) + ' minute(s) ago'
        else:
            return str(diff.seconds) + ' second(s) ago'

    def update_last_feeding_time(self):
        self.last_feeding_time = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Cat {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
