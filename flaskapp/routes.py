from flaskapp import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from flaskapp.forms import SignUp
from flaskapp.db_models import User

@app.route('/')
@app.route('/home/')
def home():
	return render_template('home.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
	form = SignUp(request.form)
	if request.method == 'POST' and form.validate():
		hashed_pass = bcrypt.generate_password_hash(form.password.data, rounds=13).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created for {form.username.data}', 'success')
		return redirect(url_for('home'))
	return render_template('sign_up.html', title='Sign Up', form=form)

