import todo_api
import datetime

if __name__ == '__main__':
	api = todo_api.ToDoApi()

	access_key = api.authorizate("login", 123456)
	# api.add_task(access_key, "make rar", datetime.datetime(2017,7,2))
	# api.change_task(access_key, 4, "completed")

	for task in (api.get_tasks(access_key, sort_by="by_completed_time")):
		print(task)
