from flaskapp.db_models import User

def user_filter(username=None, email=None):
	try:
		if username:
			return User.query.filter_by(username=username).first()
		if email:
			return User.query.filter_by(email=email).first()
	except:
		return False