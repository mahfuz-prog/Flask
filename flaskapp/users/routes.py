from flaskapp import db, bcrypt, s
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskapp.users.forms import (SignUp, LogIn, ChangeUsername, ChangePassword, 
									ResetPasswordRequest, ResetPassword)
from flaskapp.db_models import User
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.users.message_sender import send_reset_msg, verify_email_msg
from flaskapp.users.utils import user_filter

# create bluprint instance
users = Blueprint('users', __name__)

@users.route('/signup/', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = SignUp(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data, rounds=13).decode('utf-8')
		user = {'username':form.username.data, 'email': form.email.data, 'password': hashed_pass}		
		verify_email_msg(user)
		return redirect(url_for('users.login'))
	return render_template('sign_up.html', title='Sign Up', form=form)

#verification route for create account token
@users.route('/verification/<token>')
def verification(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	try:
		load_user = s.loads(token, max_age=3600)
		user = User(username=load_user['username'], email=load_user['email'], password=load_user['password'])
		db.session.add(user)
		db.session.commit()
		flash(f'Account created for {user.username}', 'success')
		return redirect('/login')
	except:
		flash(f'Account already exist, Timeout or Invalid token', 'warning')
	return redirect('/home')

@users.route('/login/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LogIn()
	if request.method == 'POST' and form.validate_on_submit():
		user = user_filter(email=form.email.data)
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('users.account'))
		else:
			flash(f'Bad credentials', 'danger')
	return render_template('login.html', title='Login', form=form)

@users.route('/logout/')
@login_required
def logout():
	logout_user()
	flash(f'You are logged out', 'success')
	return redirect('/home')

@users.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
	change_username_form = ChangeUsername()
	change_pass_form = ChangePassword()
	# have to check which form submitted by checking submit data
	if change_username_form.submit_name.data and change_username_form.validate_on_submit():
		current_user.username = change_username_form.username.data
		db.session.commit()
		flash(f'Username Changed', 'success')
		return redirect('/account')
	if change_pass_form.submit_pass.data and change_pass_form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(change_pass_form.password.data, rounds=13).decode('utf-8')
		current_user.password = hashed_pass
		db.session.commit()
		flash(f'Password Changed', 'success')
		return redirect('/account')
	return render_template('account.html', title='My Account', change_username_form=change_username_form, \
		change_pass_form=change_pass_form)

# forgot password
@users.route('/forgot-password/', methods=['GET', 'POST'])
def forgot_password():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = ResetPasswordRequest()
	if request.method == 'POST' and form.validate_on_submit():
		user = user_filter(email=form.email.data)
		send_reset_msg(user)
	return render_template('forgot_password.html', title='Forgot Password', form=form)

# verification route for reset password token
@users.route('/reset/<token>', methods=['GET', 'POST'])
def verify_reset(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token, max_age=1800)
	if user is None:
		flash(f'Timeout or invalid token', 'warning')
		return redirect('/forgot-password/')
	form = ResetPassword()
	if request.method == 'POST' and form.validate_on_submit(): 
		user.password = bcrypt.generate_password_hash(form.password.data, rounds=13).decode('utf-8')
		db.session.commit()
		flash(f'Password Changed', 'success')
		return redirect('/login')
	return render_template('verify_reset.html', title='Set Password', form=form)