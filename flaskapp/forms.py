from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskapp.db_models import User
from flaskapp import bcrypt
from flask_login import current_user

class SignUp(FlaskForm):
	username = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
		EqualTo('password', message='Passwords must match')])
	submit = SubmitField('Create Account')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already taken. Try a different one.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already taken. Try a different one.')

class LogIn(FlaskForm):
	email = StringField('User email', validators=[DataRequired(), Email()])
	password = PasswordField('User password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError('Please register first')

#Submit veriable should different for multiple form in single route
class ChangeUsername(FlaskForm):
	username = StringField('New Username', validators=[DataRequired(), Length(min=3, max=20)])
	submit_name = SubmitField('Change username')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already taken. Try a different one.')

#Submit veriable should different for multiple form in single route
class ChangePassword(FlaskForm):
	old_password = PasswordField('Current password', validators=[DataRequired()])
	password = PasswordField('New password', validators=[DataRequired()])
	submit_pass = SubmitField('Change password')

	def validate_old_password(self, old_password):
		if not bcrypt.check_password_hash(current_user.password, old_password.data):
			raise ValidationError("Password dosen't match.")

	def validate_password(self, password):
		if bcrypt.check_password_hash(current_user.password, password.data):
			raise ValidationError("Your new password is same as before! change it.")

class ResetPasswordRequest(FlaskForm):
	email = StringField('Reset password email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError('No account associated with this email')

class ResetPassword(FlaskForm):
	password = PasswordField('New password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
		EqualTo('password', message='Passwords must match')])
	submit = SubmitField('Change password')

