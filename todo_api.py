from datetime import datetime
from database import DataBase
from task import Task
from user import User


class ToDoApi:
	def __init__(self):
		self.database = DataBase('db.json')

	"""return access key for next work"""

	def authorizate(self, login, password):
		log_passw = self._logpass(login, password)
		if self.database.check_access_key(log_passw):
			return log_passw
		else:
			print("Wrong login or password")

	"""registration new users and return access key"""

	def registration(self, login, password):
		login_password = self._logpass(login, password)
		if self.database.check_access_key(login_password):
			print("This user exist")
			return None
		else:
			self.database.append_user(User(login), login_password)
			self.database.write_json()
			return login_password

	"""return task by time or/and by complete.["bytime", "bycompleted"] Example get_task(access_key, "bycompleted")"""

	def get_tasks(self, access_key, sort_by='bycompleted'):
		if self.database.check_access_key(access_key):
			return self.database.get_user(access_key).get_all_tasks(sort_by)
		else:
			print("wrong access key")

	"""add new tasks to database"""

	def add_task(self, access_key, task_title):
		if self.database.check_access_key(access_key):
			task = Task(task_title, datetime.now())
			self.database.get_user(access_key).add_task(task)
			self.database.write_json()
			print("task is added")
		else:
			print("wrong access key")

	def change_task(self, access_key, task_id, status):
		if self.database.check_access_key(access_key):
			self.database.get_user(access_key).change_task(task_id, status)
			self.database.write_json()
		else:
			print("wrong access key")

	def _logpass(self, log, passw):
		return str(log) + str(passw)
