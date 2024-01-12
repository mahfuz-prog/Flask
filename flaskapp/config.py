import os
from datetime import timedelta

class DeploymentConfig():
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	#google mail server configuration
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USERNAME = os.environ.get('EMAIL_USER') 	#email
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')	#app password
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True

class TestConfig(DeploymentConfig):
	SECRET_KEY = 'hola'
	PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
	SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"