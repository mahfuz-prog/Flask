from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flaskapp.db_models import Post

class NewPost(FlaskForm):
	title = StringField('Add post title', validators=[DataRequired()])
	description = TextAreaField('Add description', validators=[DataRequired()])
	submit = SubmitField('Add new post')

	def validate_title(self, title):
		post = Post.query.filter_by(title=title.data).first()
		if post:
			raise ValidationError('Title already taken. Try different!')

	def validate_description(self, description):
		post = Post.query.filter_by(description=description.data).first()
		if post:
			raise ValidationError('Description already taken. Try different!')


class EditPost(FlaskForm):
	title = StringField('update post title', validators=[DataRequired()])
	description = TextAreaField('update description', validators=[DataRequired()])
	submit = SubmitField('update post')