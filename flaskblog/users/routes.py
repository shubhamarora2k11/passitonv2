# -*- coding: utf-8 -*-

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__ )

from sqlalchemy import desc

@users.route('/register', methods =['GET', 'POST'])
def register():
   if current_user.is_authenticated:
       return redirect(url_for('main.home'))
   form = RegistrationForm()
   if form.validate_on_submit():
       balance = 0
       hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
       if form.designation.data == 'L' or form.designation.data == 'M' or form.designation.data == 'SSE':
           balance = 1000
       user = User(username= form.username.data, email = form.email.data, 
                   designation= form.designation.data,
                   team = form.team.data,
                   password = hashed_password,
                   balance = balance )
       db.session.add(user)
       db.session.commit()
       
       flash(f'Your account is created. You will now be able to login!', 'success')
       return redirect(url_for('users.login'))
   
   counts = User.query.order_by(desc(User.earned)).limit(5)
   return render_template('register.html', title='Register', form=form, counts=counts)


@users.route('/login', methods =['GET', 'POST'])
def login():
   if current_user.is_authenticated:
       return redirect(url_for('main.home'))
   form = LoginForm()
   if form.validate_on_submit():
       user = User.query.filter_by(email = form.email.data).first()
       if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user, remember= form.remember.data)
           next_page = request.args.get('next') 
           if next_page:
               return redirect(next_page)
           return redirect(url_for('main.home'))
       else: 
           flash(f'Login Unsuccessful. Please check your email and password!', 'danger')
       
       #if form.email.data == 'admin@myblog.com' and form.password.data == 'password':
       #    flash(f'You have been logged in!', 'success')
       #    return redirect(url_for('home'))
       #else:
       #    flash(f'Login Unsuccessful. Please check your email and password!', 'danger')
   
   counts = User.query.order_by(desc(User.earned)).limit(5)
   return render_template('login.html', title='Login', form=form, counts=counts)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route('/account' , methods =['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.designation.data = current_user.designation
        form.team.data = current_user.team
    
    eligible = User.query.filter(User.balance<1000).filter(User.balance>0).order_by(desc(User.earned))  
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file )
    counts = User.query.order_by(desc(User.earned)).limit(5)
    return render_template('account.html', title='Account', image_file=image_file, 
                           form=form, counts=counts, eligible=eligible )


@users.route('/user/<string:username>')
def user_posts(username):
   page = request.args.get('page', 1, type=int)
   user = User.query.filter_by(username=username).first_or_404()
   posts = Post.query.filter_by(author=user)\
          .order_by(Post.date_posted.desc())\
          .paginate(page=page, per_page=4)
          
   counts = User.query.order_by(desc(User.earned)).limit(5)
   return render_template('user_posts.html', posts=posts, user=user, counts=counts)


@users.route('/reset_password' , methods =['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
       return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'An email has been sent with instructions to reset your password!', 'info')
        return redirect(url_for('users.login'))
    
    counts = User.query.order_by(desc(User.earned)).limit(5)
    return render_template('reset_request.html', title='Reset Password', form=form, counts=counts)


@users.route('/reset_password/<token>' , methods =['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
       return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(f'Invalid/Expired Token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
       hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
       user.password = hashed_password
       db.session.commit() 
       flash(f'Your password has been updated. You will now be able to login!', 'success')
       return redirect(url_for('users.login'))
    
    counts = User.query.order_by(desc(User.earned)).limit(5)
    return render_template('reset_token.html', title='Reset Password', form=form, counts=counts)
