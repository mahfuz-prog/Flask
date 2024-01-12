from flaskapp.db_models import User

# helps to handle exception while filtering users
# give the ability to filter user from username or email
def user_filter(username=None, email=None):
	try:
		if username:
			return User.query.filter_by(username=username).first()
		if email:
			return User.query.filter_by(email=email).first()
	except:
		return None