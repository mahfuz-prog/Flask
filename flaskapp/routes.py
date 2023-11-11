import pyotp
from flaskapp import app, db, bcrypt, s
from flask import render_template, url_for, flash, redirect, request, abort, session
from flaskapp.forms import SignUp, LogIn, ChangeUsername, ChangePassword, ResetPasswordRequest, \
									ResetPassword, VerifyOTP
from flaskapp.db_models import User
from flask_login import login_user, current_user, logout_user, login_required, otp_required
from flaskapp.message_sender import send_reset_msg, verify_email_msg

@app.route('/')
@app.route('/home/')
def home():
	return render_template('home.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = SignUp(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data, rounds=13).decode('utf-8')
		user = {'username':form.username.data, 'email': form.email.data, 'password': hashed_pass}		
		verify_email_msg(user)
		return redirect(url_for('login'))
	return render_template('sign_up.html', title='Sign Up', form=form)

#verification route for create account token
@app.route('/verification/<token>')
def verification(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
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

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LogIn()
	if request.method == 'POST' and form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect('/account')
		else:
			flash(f'Bad credentials', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	flash(f'You are logged out', 'success')
	#return redirect(request.referrer)
	return redirect('/home')

@app.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
	change_username_form = ChangeUsername()
	change_pass_form = ChangePassword()
	#have to check which form submitted by checking submit data
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
	return render_template('account.html', title='My Account', change_username_form=change_username_form,\
	 change_pass_form=change_pass_form)

#forgot password
@app.route('/forgot-password/', methods=['GET', 'POST'])
def forgot_password():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = ResetPasswordRequest()
	if request.method == 'POST' and form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_msg(user)
	return render_template('forgot_password.html', title='Forgot Password', form=form)

#verification route for reset password token
@app.route('/reset/<token>', methods=['GET', 'POST'])
def verify_reset(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
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

#Enable two factor authentication
@app.route('/enable-two-factor/', methods=['GET', 'POST'])
@login_required
def enable_two_factor():
	if current_user.otp_secret != None:
		flash(f'Already enabled','info')
		return redirect('/account')
	if current_user.otp_secret is None:
		#this key sent to template for render with form and get back after form validation
		key = pyotp.random_base32()
		form = VerifyOTP()
		if form.validate_on_submit():
			#get the key from form
			key = request.form.get("secret")
			if pyotp.TOTP(key).verify(form.otp.data):
				current_user.otp_secret = key
				db.session.commit()
				flash(f'Successfuly enabled 2FA', 'success')
				return redirect('/account')
			else:
				flash(f'Invalid or Expired OTP', 'info')
				return redirect(url_for('enable_two_factor'))
	return render_template('MultiFA.html', title='Enable multi factor authentication', form=form, secret=key)

@app.route('/disable-two-factor/')
@login_required
def disable_two_factor():
	if current_user.otp_secret is None:
		flash('Already disabled', 'info')
		return redirect('/account')
	if current_user.otp_secret != None:
		current_user.otp_secret = None
		db.session.commit()
		flash('2FA disabled', 'success')
		return redirect('/account')

#OTP verification
@app.route('/verify-otp/', methods=['POST', 'get'])
@login_required
def verify_otp_form():
	if current_user.otp_secret is None:
		flash('2FA disabled. Please enable first', 'info')
		return redirect('/account/')

	form = VerifyOTP()
	if form.validate_on_submit():
		session.pop(f'{current_user.id}_otp', None)
		session[f'{current_user.id}_otp'] = form.otp.data
		next_page = request.args.get('next')
		return redirect(next_page) if next_page else redirect('/account')
	return render_template('verify_otp.html', title="OTP verification", form=form)

# to access this route need login_required and otp_required
@app.route('/secure-page/', methods=['GET', 'POST'])
@login_required
@otp_required
def secure_page():
	return 'secure data'