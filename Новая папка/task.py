import datetime
class Task:
	def __init__(self, task='', start_time='', json_load=None):
		if json_load is not None:
			self.__dict__ = json_load
		else:
			self.name = task
			self.start_time = start_time
			self.complete = "active"
			self.id = 0

	def __repr__(self):
		return "{0} {1} {2} task id: {3}".format(self.name, self.start_time, self.complete, self.id)
