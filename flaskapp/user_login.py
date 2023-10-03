from flask_login import UserMixin
from flaskapp import login_manager

# Mock database
users = {'webwaymark@gmail.com': {'password': 'asd'}, 'mahfuz@gmail.com': {'password': 'asd'}}

@login_manager.user_loader
def user_loader(email):
    user = User()
    user.id = email
    return user

class User(UserMixin):
    pass