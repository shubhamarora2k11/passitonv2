# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Associate Email' , render_kw={'readonly': True})
    category = SelectField(
        'Category of Achievement',
        choices=[("Excellence", 'Excellence'), ("Ownership", 'Ownership'),
                 ("Support", 'Support'), ('Passion','Passion')]
        )   
    content = TextAreaField('Content', validators=[ DataRequired() ] )
    submit = SubmitField('Post')
    