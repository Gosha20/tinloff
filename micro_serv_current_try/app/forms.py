from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField(
		'Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')


class AddTaskForm(FlaskForm):
	task_body = StringField("TaskBody", validators=[DataRequired()])
	submit = SubmitField('Add')


class ChangeTaskForm(FlaskForm):
	task_id = IntegerField("TaskId", validators=[DataRequired()])
	task_status = StringField("TaskStatus", validators=[DataRequired()])
	submit = SubmitField('Change')
