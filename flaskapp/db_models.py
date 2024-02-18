from flaskapp import db, login_manager, s
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def user_loader(user_id):
    # user = User.query.get(int(user_id)int(user_id))
    user = db.session.get(User, int(user_id))
    return user

class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	# forgot password token
	def create_token(self):
		return s.dumps({'user_id': self.id})

	# verify forgot password token
	@staticmethod
	def verify_reset_token(token, max_age=120):
		try:
			user_id = s.loads(token, max_age=max_age)['user_id']
		except:
			return None
		# return User.query.get(user_id)
		return db.session.get(User, int(user_id))

	def __repr__(self):
		return f'username: {self.username} | email: {self.email}'

class Post(db.Model):
	__tablename__ = 'post'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), unique=True, nullable=False)
	description = db.Column(db.Text, unique=True, nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f'title: {self.title}'