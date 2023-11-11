from flask_mail import Message
from flaskapp import s, mail
from flask import url_for, flash
#account email confirmation sender
def verify_email_msg(user):
	token = s.dumps(user)
	msg = Message('Confirm email', sender='noreply@demo.com', recipients=[user['email']])
	msg.body = f'''To confirm your email, visit the following link:
{url_for('verification', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
	try:
		mail.send(msg)
		flash('An email has been sent with instructions to confirm email.', 'info')
	except Exception as e:
		flash(f"Mail dosen't send. Try again.", 'warning')

#reset password email sender
def send_reset_msg(user):
	token = user.create_token()
	msg = Message('Reset password', sender='noreply@demo.com', recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link:
{url_for('verify_reset', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
	try:
		mail.send(msg)
		flash('An email has been sent with instructions to reset password. The token will expire after 30 minutes.', 'info')
	except Exception as e:
		flash(f"Mail dosen't send. Try again.", 'warning')

#send otp
def send_otp(otp, email):
	msg = Message('OTP', sender='noreply@demo.com', recipients=[email])
	msg.body = f'''Your otp is: { otp }.If you did not make this request then simply ignore this email and no changes will be made.
'''
	try:
		mail.send(msg)
		flash('An email has been sent with OTP. The OTP will expire after 30 seconds.', 'info')
		return True
	except Exception as e:
		print(e)
		flash(f"Mail dosen't send. Try again.", 'warning')
		return False