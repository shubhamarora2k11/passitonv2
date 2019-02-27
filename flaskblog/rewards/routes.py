# -*- coding: utf-8 -*-

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Reward, User, Post
from flaskblog.rewards.forms import RewardForm, DashboardForm, SearchAssociateForm,RedirectForm

rewards = Blueprint('rewards', __name__ )
from flaskblog.users.utils import send_reward_email

from sqlalchemy import desc

 
@rewards.route('/reward/new' , methods =['GET', 'POST'])
@login_required
def new_reward():   
    form = RewardForm()
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file )
    if form.validate_on_submit():
        reward = Reward(associate_id=form.associate_id.data, category=form.category.data, reward_points=form.reward_points.data, giver=current_user)
        db.session.add(reward)
        current_user.balance = current_user.balance - form.reward_points.data
        associate = User.query.filter_by(email=form.associate_id.data).first()
        associate.earned = associate.earned + form.reward_points.data
        from_user= current_user.email
        title= ' received recognition for his/her efforts from @'+str(current_user.username)
        content ='Category: '+str(form.category.data)+'\n' + form.reward_comments.data
        post = Post(title=title, content=content, author=associate, from_user=from_user)
        db.session.add(post)
        db.session.commit()
        
        send_reward_email(associate, current_user)
        
        flash(f'Your reward has been shared successfully!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        user_email = request.args.get('user_email', None)
        print(user_email)
        form.associate_id.data = user_email
        user = User.query.filter_by(email=user_email).first()
        form.associate_name.data = user.username
        form.balance.data = current_user.balance
        image_file = url_for('static', filename='profile_pics/'+ user.image_file )
    counts = User.query.order_by(desc(User.earned)).limit(5)
    return render_template('create_reward.html', title='New Reward', form=form,
                           legend='New Reward', image_file=image_file, counts=counts)

@rewards.route('/reward/search' , methods =['GET', 'POST'])
@login_required
def search_associate():   
    form = SearchAssociateForm()
    if form.validate_on_submit():
        associate = User.query.filter_by(email=form.associate_id.data).first()
        print(associate)    
        return redirect(url_for('rewards.typeofreward', user_email = associate.email))
    counts = User.query.order_by(desc(User.earned)).limit(5)
    eligible = User.query.filter(User.balance<1000).filter(User.balance>0).order_by(desc(User.earned))
    eligible = current_user.rewards
    templist=[]
    for reward in eligible:
        temp =  User.query.filter(User.email==reward.associate_id).first()
        templist.append(temp)
       
    eligible = templist
    
    #print(counts)
    return render_template('search_associate.html', title='New Reward', form=form, 
                           legend='Search Associate', counts=counts, eligible=eligible)


@rewards.route('/dashboard' , methods =['GET', 'POST'])
@login_required
def dashboard():
    form = DashboardForm()
    counts = User.query.order_by(desc(User.earned)).limit(5)
    if request.method == 'GET':
        form.earned.data = current_user.earned
        form.balance.data = current_user.balance
        #eligible = User.query.filter(User.balance<1000).filter(User.balance>0).order_by(desc(User.earned))
   
        if current_user.is_authenticated:
            eligible = current_user.rewards
            templist=[]
            for reward in eligible:
                temp =  User.query.filter(User.email==reward.associate_id).first()
                templist.append(temp)
       
            eligible = templist
            if current_user.designation == 'M' or current_user.designation == 'L' or current_user.designation == 'SSE':
                return render_template('dashboard.html', title='Dashboard', form=form, 
                                       counts=counts, eligible=eligible,
                                       legend='Redeem Points', legend2='Share Points'
                                       )
            else:
                return render_template('dashboard.html', title='Dashboard', form=form, 
                           counts=counts, legend='Redeem Points', legend2='Share Points')
        else:
            return render_template('dashboard.html', title='Dashboard', form=form, 
                          counts=counts, legend='Redeem Points', legend2='Share Points')
    
    elif form.validate_on_submit():
        print("2:"+str(form.submit2.data))
        print("1:"+str(form.submit.data))
        if(form.submit.data):
            return "Feature will be added soon"
        elif(form.submit2.data):
            return redirect(url_for('rewards.search_associate'))
        
        
    
    return render_template('dashboard.html', title='Dashboard', form=form, 
                           legend='Redeem Points', legend2='Share Points', counts=counts)



@rewards.route('/reward/history/')
@login_required
def history():
   page = request.args.get('page', 1, type=int)
   posts = Reward.query.filter(Reward.associate_id == current_user.email).order_by(desc(Reward.date_of_reward)).paginate(page=page, per_page=5)
   counts = User.query.filter(User.earned>0).order_by(desc(User.earned)).limit(5)
   #print(counts.all(), eligible.all())
   print(current_user)
   print(posts.items)
   eligible = current_user.rewards
   templist=[]
   for reward in eligible:
       temp =  User.query.filter(User.email==reward.associate_id).first()
       templist.append(temp)
       
   eligible = templist
   if current_user.designation == 'M' or current_user.designation == 'L' or current_user.designation == 'SSE':
       return render_template('history.html', posts=posts, counts=counts, eligible = eligible )
   else:
       return render_template('history.html', posts=posts, counts=counts)


@rewards.route('/reward/typeofreward/', methods =['GET', 'POST'])
@login_required
def typeofreward():   
    form = RedirectForm()
    if request.method == 'GET':
        user_email = request.args.get('user_email', None)
        print(user_email)
        form.associate_id.data = user_email
        user = User.query.filter_by(email=user_email).first()
        form.associate_name.data = user.username
        image_file = url_for('static', filename='profile_pics/'+ user.image_file )
    
    elif form.validate_on_submit():
        #print("2:"+str(form.submit2.data))
        #print("1:"+str(form.submit.data))
        user_email = request.args.get('user_email', None)
        
        if(form.submit.data):
            return redirect(url_for('posts.new_post', user_email = user_email))
        elif(form.submit2.data):
            return redirect(url_for('rewards.new_reward', user_email = user_email))
        
    counts = User.query.order_by(desc(User.earned)).limit(5)
    return render_template('redirect.html', title='Reward Type', form=form,
                           legend= 'Reward Type', image_file=image_file, counts=counts)
