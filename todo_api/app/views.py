from flask import request, jsonify, make_response
from pytz import unicode
from app import app, db, nice_json, SORTED_FUNC
from app.models import User, Task
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
	user = User.query.filter_by(username=username).first()
	if user is not None:
		return user.password_hash
	else:
		return None


@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(400)
def bad_request(error='Bad request'):
	return make_response(jsonify({'error': error}), 400)


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
	key_sort = request.args.get('sort', default='by_completed')
	user = User.query.filter_by(username=auth.get_auth()['username']).first()
	tasks = user.tasks.all()
	data = nice_json(tasks)
	return jsonify({'tasks': sorted(data, key=SORTED_FUNC[key_sort])})


@app.route('/todo/api/v1.0/registration', methods=['POST'])
def registration():
	if not request.json or not 'login' in request.json or not 'password' in request.json:
		return bad_request()
	if User.query.filter_by(username=request.json['login']).first() is not None:
		return bad_request('user exist')
	else:
		user = User(username=request.json['login'])
		user.set_password(request.json['password'])
		db.session.add(user)
		db.session.commit()
		return jsonify(request.json), 201


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
	if not request.json or not 'body' in request.json:
		return bad_request()
	user_id = User.query.filter_by(username=auth.get_auth()['username']).first().id
	task = Task(body=request.json['body'], user_id=user_id)
	db.session.add(task)
	db.session.commit()
	return jsonify({'task': nice_json([task])}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
	user = User.query.filter_by(username=auth.get_auth()['username']).first()
	tasks = list(filter(lambda x: x.id == task_id, user.tasks.all()))
	if 0 == len(tasks) or len(tasks) > 1:
		return bad_request('Invalid task_id')
	if not request.json:
		return bad_request('Invalid json')
	if 'body' in request.json and type(request.json['title']) is not unicode:
		return bad_request('Invalid body')
	if 'status' in request.json and type(request.json['status']) is not unicode:
		return bad_request('Invalid status')
	task = tasks[0]
	task.body = request.json.get('body', task.body)
	task.status = request.json.get('status', task.status)
	db.session.commit()
	return jsonify({'task': nice_json([task])})


