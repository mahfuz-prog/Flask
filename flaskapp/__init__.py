from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous.url_safe import URLSafeTimedSerializer
from flaskapp.config import DeploymentConfig, TestConfig

# application factory
config_class = DeploymentConfig

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
s = URLSafeTimedSerializer(config_class.SECRET_KEY)
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "users.login"
login_manager.login_message = u"Login required"
login_manager.login_message_category = 'info'

def create_app(config_class=config_class):
	app = Flask(__name__)
	app.config.from_object(config_class)

	mail.init_app(app)
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)

	# register blueprint to application
	from flaskapp.main.routes import main
	from flaskapp.users.routes import users
	from flaskapp.posts.routes import posts
	from flaskapp.errors.handlers import errors
	app.register_blueprint(main)
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(errors)
	
	with app.app_context():
		# db.drop_all()
		db.create_all()
	print('Config class: ', config_class)
	return app