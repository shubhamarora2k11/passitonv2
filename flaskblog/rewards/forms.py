# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email
from flask_login import current_user
from flaskblog.models import User, Reward
from datetime import datetime
from datetime import timedelta
from sqlalchemy import desc


class RedirectForm(FlaskForm):
    associate_id = StringField('Associate Email', render_kw={'readonly': True}) 
    associate_name = StringField('Associate Name', render_kw={'readonly': True}) 
    #StringField('Category of Award', validators=[ DataRequired() ]) 
    
    submit = SubmitField('Appreciate Peer')
    submit2 = SubmitField('Share Reward')
    
    #email = User.query.filter_by(email=associate_id.data).first()
        
    #last_reward = Reward.query.filter(User.email==Reward.associate_id).filter(Reward.date_of_reward >= datetime.utcnow() + timedelta(days=-30)).filter(User.email==email.email).first()
    #if last_reward is not None:
    #    raise ValidationError('Associate already got rewarded for this month')
    


class RewardForm(FlaskForm):
    associate_id = StringField('Associate Email', render_kw={'readonly': True}) 
    associate_name = StringField('Associate Name', render_kw={'readonly': True}) 
    category = SelectField(
        'Category of Achievement',
        choices=[("Excellence", 'Excellence'), ("Ownership", 'Ownership'),
                 ("Support", 'Support'), ('Passion','Passion')]
        )
    #StringField('Category of Award', validators=[ DataRequired() ]) 
    balance = IntegerField('Balance', render_kw={'readonly': True})
    reward_points = IntegerField('Points to be shared', validators=[ DataRequired()  ] )
    reward_comments = TextAreaField('Reward Comments (Optional)' )
    submit = SubmitField('Share Reward')

	
    def validate_reward_points(self, reward_points):
        print(current_user.balance , reward_points.data)
        if int(current_user.balance) < int(reward_points.data):
            raise ValidationError('Insufficient Funds!')

class SearchAssociateForm(FlaskForm):
    associate_id = StringField('Associate Email', validators=[ DataRequired(), Email() ]) 
    submit = SubmitField('Search Associate')

    def validate_associate_id(self, associate_id):
        if associate_id.data==current_user.email:
            raise ValidationError('Too Smart! but you cannot search yourself :D')
        email = User.query.filter_by(email=associate_id.data).first()
        if email:
            last_reward = Reward.query.filter(Reward.giver==current_user).filter(Reward.associate_id==email.email).order_by(desc(Reward.date_of_reward)).first()
            
        if email is None:
            raise ValidationError('Email does not exist, please choose a genuine one')
        #elif email.team != current_user.team:
            #raise ValidationError('Associate doesnt belong to the same team')
        elif last_reward is not None:
            raise ValidationError('Associate already got rewarded for this month')
            
            
class DashboardForm(FlaskForm):
    earned = IntegerField('Earned Points', render_kw={'readonly': True})
    submit = SubmitField('Redeem Reward Points')
    balance = IntegerField('Balance Points', render_kw={'readonly': True})
    submit2 = SubmitField('Share Reward Points')
    
    

        