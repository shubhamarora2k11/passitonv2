# -*- coding: utf-8 -*-
from flask import render_template, request, Blueprint
from flaskblog.models import Post, User,Reward
from flask_login import login_required, current_user

main = Blueprint('main', __name__ )

from sqlalchemy import desc

@main.route('/')
@main.route('/home')
def home():
   page = request.args.get('page', 1, type=int)
   
   if current_user.is_authenticated:
       posts = Post.query.filter(User.id==Post.user_id).filter(User.team == current_user.team).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
   else:
       posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
       
   counts = User.query.filter(User.earned>0).order_by(desc(User.earned)).limit(5)
   
   #print(counts.all(), eligible.all())
   print(current_user)
   
   if current_user.is_authenticated:
       eligible = current_user.rewards
       templist=[]
       for reward in eligible:
           temp =  User.query.filter(User.email==reward.associate_id).first()
           templist.append(temp)
       
       eligible = templist
       if current_user.designation == 'M' or current_user.designation == 'L' or current_user.designation == 'SSE':
           return render_template('home.html', posts=posts, counts=counts, eligible = eligible )
       else:
           return render_template('home.html', posts=posts, counts=counts)
   else:
       return render_template('home.html', posts=posts, counts=counts)

@main.route('/all')
def home_all():
   page = request.args.get('page', 1, type=int)
   posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
       
   counts = User.query.filter(User.earned>0).order_by(desc(User.earned)).limit(5)
   
   #print(counts.all())
   

   if current_user.is_authenticated:
       eligible = current_user.rewards
       templist=[]
       for reward in eligible:
           temp =  User.query.filter(User.email==reward.associate_id).first()
           templist.append(temp)
       
       eligible = templist
       
       if current_user.designation == 'M' or current_user.designation == 'L' or current_user.designation == 'SSE':
           return render_template('home.html', posts=posts, counts=counts, eligible = eligible )
       else:
           return render_template('home.html', posts=posts, counts=counts)
   else:
       return render_template('home.html', posts=posts, counts=counts)
