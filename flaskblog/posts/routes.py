# -*- coding: utf-8 -*-

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, User
from flaskblog.posts.forms import PostForm


posts = Blueprint('posts', __name__ )

from sqlalchemy import desc

@posts.route('/post/new/' , methods =['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        associate = User.query.filter_by(email=form.title.data).first()
        title= ' received recognition for his/her efforts from @'+str(current_user.username)
        content ='Category: '+str(form.category.data)+'\n' + form.content.data
        from_user = current_user.email
        post = Post(title=title, content=content, author=associate, from_user=from_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        user_email = request.args.get('user_email', None)
        print(user_email)
        form.title.data = user_email
    counts = User.query.order_by(desc(User.earned)).limit(5)
    return render_template('create_post.html', title='New Post', form=form, 
                           legend='New Post', counts=counts)

@posts.route('/post/<int:post_id>' , methods =['GET', 'POST'])
#@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    counts = User.query.order_by(desc(User.earned)).limit(5)
    return render_template('post.html', title=post.title, post=post, counts=counts)
    
@posts.route('/post/<int:post_id>/update' , methods =['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.from_user!=current_user.email:
        abort(403)
    form= PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id= post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    counts = User.query.order_by(desc(User.earned)).limit(5)
    return render_template('create_post.html', title='Update Post', form=form,
                           legend='Update Post', counts=counts)

@posts.route('/post/<int:post_id>/delete' , methods =['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.from_user!=current_user.email:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post has been deleted!', 'success')
    
    return redirect(url_for('main.home'))


