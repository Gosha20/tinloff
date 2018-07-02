import datetime
import json

from task import Task
from user import User


class DataBase:
	def __init__(self, file):
		self._users = dict()
		self.load_json(file)

	def get_user(self, acces_key):
		return self._users[acces_key]

	def append_user(self, user, index):
		self._users[index] = user

	def check_access_key(self, access_key):
		return access_key in self._users.keys()

	def load_json(self, file):
		try:
			with open(file, 'r') as f:
				data = f.read()
				loads_data = json.loads(data)
				for log_passw, user in loads_data.items():
					des_user = User(json_load=user)
					temp_tasks_dict = dict()
					for task_id, task in user['to_do'].items():
						des_task = Task(json_load=task)
						temp_tasks_dict[int(task_id)] = des_task
					des_user.to_do = temp_tasks_dict
					self._users[log_passw] = des_user
				print("loaded")
		except FileNotFoundError:
			print("file not found")
		except ValueError:
			print("cant load json file")

	def write_json(self, file='db.json'):
		try:
			with open(file, 'w') as f:
				data = json.dumps(self._users,
								  default=lambda x: x.isoformat() if isinstance(x, datetime.datetime) else x.__dict__,
								  sort_keys=True,
								  indent=4)
				f.write(data)
		except TypeError:
			print("not serialize obj")
