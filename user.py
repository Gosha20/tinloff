class User:
	SORTED_FUNC = {
		'bytime': lambda task: task.start_time,
		'bycompleted': lambda task: task.complete != "completed"
	}

	def __init__(self, name='', json_load=None):
		if json_load is not None:
			self.__dict__ = json_load
		else:
			self.name = name
			self.to_do = dict()

	def add_task(self, task):
		task.id = self._get_index()
		self.to_do[task.id] = task

	def delete_task(self, task_id):
		self.to_do.pop(task_id, None)

	def get_all_tasks(self, sort_by="bycompleted"):
		return sorted(self.to_do.values(), key=User.SORTED_FUNC[sort_by])

	def change_task(self, task_id, status):
		if task_id in self.to_do:
			self.to_do[task_id].complete = status
			return "task is changed"
		else:
			return "not exist this task id"

	def _get_index(self):
		return len(self.to_do)

	def __repr__(self):
		return "{0} {1}".format(self.name, self.to_do)
