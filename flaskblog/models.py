from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    designation = db.Column(db.String(15), nullable=False)
    team = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    earned = db.Column(db.Integer, nullable=False, default=0)
    posts = db.relationship('Post', backref='author', lazy=True)
    rewards = db.relationship('Reward', backref='giver', lazy=True)
    #notifications =  db.relationship('Notification', backref='receiver', lazy=True)
	
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.designation}', '{self.team}', '{self.image_file}')"
		
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    from_user = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    associate_id = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    date_of_reward = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    reward_points = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
    def __repr__(self):
        return f"Reward('{self.associate_id}', '{self.reward_points}', '{self.date_of_reward}')"
    
