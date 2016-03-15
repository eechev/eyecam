from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Cameras(db.Model):
    __tablename__ = 'cameras'
    id = db.Column(db.Integer, primary_key=True)
    cameraName = db.Column(db.String(10), unique=True, index=True)
    resolution = db.Column(db.Enum('low', 'medium', 'high'), unique=False)
    vflip = db.Column(db.Boolean, unique=False, default=False)
    hflip = db.Column(db.Boolean, unique=False, default=False)
    