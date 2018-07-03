import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, nice_json, SORTED_FUNC
from app.forms import LoginForm, RegistrationForm, AddTaskForm, ChangeTaskForm
from app.models import User, Task


@app.route('/')
@app.route('/index')
@login_required
def index():
	user = current_user
	return render_template("index.html", title='Home', user=user, db=user.tasks.all())


@app.route('/index/get_json')
@login_required
def get_json():
	user = current_user
	tasks = user.tasks.all()
	data = nice_json(tasks)
	try:
		sorted_key = request.url.split('?')[1]
	except IndexError:
		return jsonify(data)

	if data is not None:
		return jsonify(sorted(data, key=SORTED_FUNC[sorted_key]))
	else:
		return jsonify(None)


@app.route('/index/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
	user = current_user
	form = AddTaskForm()
	if form.validate_on_submit():
		task = Task(body=form.task_body.data, timestamp=datetime.datetime.utcnow(), user_id=user.id)
		db.session.add(task)
		db.session.commit()
		flash('Congratulations, you are now add task!')
		return render_template("add_task.html", title='Add', form=form)
	else:
		return render_template("add_task.html", title='Add', form=form)


@app.route('/index/change_task', methods=['GET', 'POST'])
@login_required
def change_task():
	user = current_user
	form = ChangeTaskForm()
	if form.validate_on_submit():
		tasks = list(filter(lambda x: x.id == form.task_id.data, user.tasks.all()))
		if 0 == len(tasks) or len(tasks) > 1:
			flash('Invalid task_id')
			return redirect(url_for('change_task'))
		task = tasks[0]
		task.status = form.task_status.data
		db.session.commit()
		flash('Congratulations, you are now change task!')
		return render_template("change_task.html", title='Change', form=form)
	else:
		return render_template("change_task.html", title='Change', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)
