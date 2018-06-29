import todo_api

if __name__ == '__main__':
	api = todo_api.ToDoApi()

	access_key = api.registration("login", 123456)
	api.add_task(access_key, "make sandwich")
	api.change_task(access_key, 0, "completed")

	for task in (api.get_tasks(access_key, sort_by="bycompleted")):
		print(task)
