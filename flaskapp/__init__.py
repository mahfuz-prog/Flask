import os
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message = u"Login required"
login_manager.login_message_category = 'info'

from flaskapp.routes import app