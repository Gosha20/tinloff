from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

def nice_json(arg):
	try:
		tempList = []
		for task in arg:
			tempDict = {
				'id': task.id,
				'body': task.body,
				'status': task.status,
				'timestamp': task.timestamp}
			tempList.append(tempDict)
		return tempList
	except TypeError:
		return {}

SORTED_FUNC = {
		'by_time': lambda task: task['timestamp'],
		'by_completed': lambda task: task['status'] != "completed",
		'by_completed_time': lambda task: tuple((task['status'] != "completed", task['timestamp']))
	}

from app import views, models
