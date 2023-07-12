from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,PasswordField
from wtforms.validators import DataRequired,EqualTo
from flask_wtf.file import FileField






class Search_Form(FlaskForm):
    searched=StringField(label='searched',validators=[DataRequired(),])
    submit=SubmitField(label='Submit')



class PostsForm(FlaskForm):
    title=StringField(label='title',validators=[DataRequired(),])
    content=TextAreaField(label='Content',validators=[DataRequired(),])
    slug=StringField(label='Slug',validators=[DataRequired(),])
    submit=SubmitField(label='Submit')



class Name_Form(FlaskForm):
    name=StringField(label='what your name ?: ',validators=[DataRequired(),])
    submit=SubmitField(label='Submit : ')



class User_Form(FlaskForm):
    user_name=StringField(label='user name :',validators=[DataRequired()])
    name=StringField(label='Name :',validators=[DataRequired()])
    email=StringField(label='Email id :',validators=[DataRequired()])
    password=PasswordField(label='password',validators=[DataRequired(),EqualTo('password_2',message='password most match !!')])
    password_2=PasswordField(label='confirm password',validators=[DataRequired(),])
    favorite_color=StringField(label='write color :')
    about_author=TextAreaField(label='about author:')
    profile_pic=FileField(label='profile pic')
    submit=SubmitField(label='Submit')


class PasswordForm(FlaskForm):
    email=StringField(label='email address',validators=[DataRequired(),])
    password_hash=PasswordField(label='password',validators=[DataRequired()])
    submit=SubmitField(label='check password')

class LoginForm(FlaskForm):
    user_name=StringField(label='User Name',validators=[DataRequired()])
    password=PasswordField(label='Password',validators=[DataRequired()])
    submit=SubmitField(label='sing in')

