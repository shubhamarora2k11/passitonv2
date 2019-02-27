# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[ DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    designation = SelectField(
        'Designation',
        choices=[("I", 'Intern'), ("SE", 'Software Engineer'),
                 ("ASSE", 'Associate Senior Software Engineer'), ('SSE','Senior Software Engineer'),
                 ("L","Lead"), ("M","Manager")
                 ]
        )
    team = SelectField(
        'Team',
        choices=[("ITWorks", 'ITWorks'), ("RevWorks", 'RevWorks'),
                 ("IP", 'IP'), ("Development", 'Development') 
                 ]
        )
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken, please choose a different one')
            
    def validate_email(self, email):        
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email is taken, please choose a different one')
	

class LoginForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', render_kw={'readonly': True})
    email = StringField('Email', render_kw={'readonly': True}) 
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    designation = StringField('Designation', render_kw={'readonly': True}) 
    team = StringField('Team', render_kw={'readonly': True}) 
    
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data!= current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken, please choose a different one')
                
    def validate_email(self, email):       
        if email.data!= current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email is taken, please choose a different one')



class RequestResetForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
             
    def validate_email(self, email):        
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('There is no account with the specified email. You must register first!')
	
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')