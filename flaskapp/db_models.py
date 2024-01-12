from flaskapp import db, login_manager, s
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    user = User.query.get(int(user_id))
    return user

class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

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
		return User.query.get(user_id)

	def __repr__(self):
		return f'username: {self.username} | email: {self.email}'