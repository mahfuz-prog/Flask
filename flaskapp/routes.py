from flaskapp import app
from flask import render_template, flash, request, redirect
from flaskapp.user_login import User, users
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.forms import LogIn

@app.route('/')
@app.route('/home/')
def home():
	return render_template('home.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect('/home')
	form = LogIn()
	if request.method == 'POST' and form.validate():
		email = form.email.data
		if (email in users) and (users[email]['password'] == form.password.data):
			user = User()
			user.id = email
			login_user(user, remember=form.remember.data)
			flash(f'Logged in as {email}', 'success')
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect('/home')
		else:
			flash(f'Bad credentials', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	flash(f'You are logged out', 'success')
	return redirect(request.referrer)
