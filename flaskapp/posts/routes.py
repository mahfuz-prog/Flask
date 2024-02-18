from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, session
from flask_login import current_user, login_required
from flaskapp.posts.forms import NewPost, EditPost
from flaskapp.db_models import Post
from flaskapp import db

posts = Blueprint('posts', __name__, url_prefix='/posts')

@posts.route('/')
def blog():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=9)
	return render_template('posts/blog.html', title='Blog', posts=posts)

# add new post
@posts.route('/new/', methods=['GET', 'POST'])
@login_required
def new_post():
	form = NewPost()
	if request.method == 'POST' and form.validate_on_submit():
		title = form.title.data.replace('-', ' ')
		post = Post(title=title, description=form.description.data, author=current_user)
		db.session.add(post)
		try:
			db.session.commit()
			flash(f'{form.title.data} post added.', 'info')
		except Exception as e:
			flash(f'{e}', 'danger')
		return redirect(url_for('posts.blog'))

	return render_template('posts/new_post.html', title='New Post', form=form)

# single post page
@posts.route('/<int:post_id>/<title>/')
def read(post_id, title):
	post = Post.query.get_or_404(post_id)
	# check the title if it containing valid data or not
	if title.replace('-', ' ') not in post.title:
		abort(404)
	return render_template('posts/single_post.html', title=title, post=post)

# edit a post
@posts.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(401)
	form = EditPost()
	if form.validate_on_submit():
		post.title = form.title.data
		post.description = form.description.data
		db.session.commit()
		flash('Post updated', 'info')
		return redirect(url_for('posts.read', post_id=post_id, title=post.title.replace(' ', '-')))
	elif request.method == 'GET':
		form.title.data = post.title
		form.description.data = post.description
	return render_template('posts/edit.html', title='Edit post', form=form, post=post)

# delete a post
@posts.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(401)
	db.session.delete(post)
	db.session.commit()
	flash(f'{post.title} Deleted', 'success')
	return redirect(url_for('users.account'))