from datetime import datetime
from app import db
from hashlib import sha256


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	tasks = db.relationship('Task', backref='author', lazy='dynamic')

	def __repr__(self):
		return '<User {}, passw_hash {}>'.format(self.username, self.password_hash)

	def set_password(self, password):
		self.password_hash = str(password)

	def check_password(self, password):
		return sha256(password) == self.password_hash


class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	status = db.Column(db.String(40), default="active")

	def __repr__(self):
		return '<{} Task {}, time created {}, status {}>'.format(self.id, self.body, self.timestamp, self.status)
