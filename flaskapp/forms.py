from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email
from flaskapp.user_login import users

class LogIn(FlaskForm):
	email = StringField('User email', validators=[DataRequired(), Email()])
	password = PasswordField('User password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')

	def validate_email(self, email):
		if email.data not in users:
			raise ValidationError('Please register first')
