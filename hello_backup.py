from flask import Flask,render_template,session,flash,redirect,url_for,request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,EmailField,TextAreaField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired,Email,EqualTo,Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import date
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user


app=Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY']='0126404027'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///user.db'

db=SQLAlchemy(app)
migrate=Migrate(app,db)
login_manger=LoginManager(app)

login_manger.login_view='login'


@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255))
    content=db.Column(db.Text)
    author=db.Column(db.String(255))
    date_posted=db.Column(db.DateTime,default=datetime.utcnow())
    slug=db.Column(db.String(255))


class PostsForm(FlaskForm):
    title=StringField(label='title',validators=[DataRequired(),])
    content=TextAreaField(label='Content',validators=[DataRequired(),])
    author=StringField(label='Author',validators=[DataRequired(),])
    slug=StringField(label='Slug',validators=[DataRequired(),])
    submit=SubmitField(label='Submit')





class User(db.Model,UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(300),nullable=False,unique=True)
    name=db.Column(db.String(300),nullable=False)
    email=db.Column(db.String(300),nullable=False,unique=True)
    favorite_color=db.Column(db.String(120))
    date_added=db.Column(db.DateTime,default=date.today())
    password_hash=db.Column(db.String,nullable=False)


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute !')


    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password=password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)



    def __repr__(self):
        return f'{self.name}'


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
    submit=SubmitField(label='Submit')


class PasswordForm(FlaskForm):
    email=StringField(label='email address',validators=[DataRequired(),])
    password_hash=PasswordField(label='password',validators=[DataRequired()])
    submit=SubmitField(label='check password')

class LoginForm(FlaskForm):
    user_name=StringField(label='User Name',validators=[DataRequired()])
    password=PasswordField(label='Password',validators=[DataRequired()])
    submit=SubmitField(label='sing in')


@app.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(user_name=form.user_name.data).first()
        if user !=None:
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash('login seccessfull !')
                return redirect(url_for('dashboard'))

            else:
                flash('wrong password try agine!')

        else:
            flash('wrong user name try agine !')


    return render_template('login.html',form=form)



@app.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    flash('you have been log out ! thanks for stoping by ')
    return redirect(url_for('login'))

@app.route('/dashboard',methods=['POST','GET'])
@login_required
def dashboard():
    form = User_Form()
    id=current_user.id
    name_to_update = User.query.get_or_404(id)

    if request.method == 'POST':
        name_to_update.user_name = request.form['user_name']
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.password = request.form['password']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash('User update successfully')
            return redirect(url_for("added_user"))
            # return render_template('update.html', form=form, name_to_update=name_to_update)

        except:
            flash('error somthing went roung plese tay agine letter')
            return render_template('dashboard.html', form=form, name_to_update=name_to_update)

    else:
        return render_template('dashboard.html', form=form, name_to_update=name_to_update, user_id=id)





@app.route('/posts')
def posts():

    posts=Posts.query.all()

    return render_template('posts.html',posts=posts)


@app.route('/post/delete/<int:id>')
def delete_post(id):
    post_to_delete=Posts.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()

        flash('post hase been deleted')

        posts=Posts.query.all()

        return render_template('posts.html',posts=posts)
    except:
        flash('somthing went wrong plase tey agine')
        posts = Posts.query.all()

        return render_template('posts.html', posts=posts)





@app.route('/post/<int:id>')
@login_required
def post(id):
    the_post=Posts.query.get_or_404(id)

    return render_template('post.html',post=the_post)




@app.route('/post/edit/<int:id>' ,methods=['POST','GET'])
@login_required
def edit_post(id):
    post=Posts.query.get_or_404(id)
    form=PostsForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.author=form.author.data
        post.slug=form.slug.data
        post.content=form.content.data
        try:
            db.session.add(post)
            db.session.commit()
            flash('update post compleate')
            return redirect(url_for('post',id=post.id))

        except:
            flash('somthing went wronge , plase try agine')
            return redirect(url_for('posts',id=post.id))

    form.title.data=post.title
    form.author.data=post.author
    form.slug.data=post.slug
    form.content.data= post.content
    return render_template('edit_post.html',form=form,post=post)





@app.route('/add_post',methods=['POST','GET'])
def add_post():
    form=PostsForm()

    if form.validate_on_submit():
        posts=Posts(title=form.title.data,author=form.author.data,
                    content=form.content.data,slug=form.slug.data)
        form.title.data=''
        form.author.data=''
        form.slug.data=''
        form.content.data=''

        db.session.add(posts)
        db.session.commit()

        flash('blog post submitted seccessfully')

        return redirect(url_for('posts'))



    return render_template('add_post.html',form=form)



@app.route('/date')
def curent_date():
    return {"date":date.today()}




@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete=User.query.get_or_404(id)


    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('user hase been deleted !!')
        return redirect(url_for("added_user"))
        # return render_template('update.html', form=form, name_to_update=name_to_update)



    except:
        flash('whooops! there is problem deleting this user')



@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    form=User_Form()
    name_to_update=User.query.get_or_404(id)

    if request.method=='POST':
        name_to_update.user_name=request.form['user_name']
        name_to_update.name=request.form['name']
        name_to_update.email=request.form['email']
        name_to_update.password=request.form['password']
        name_to_update.favorite_color=request.form['favorite_color']
        try:
            db.session.commit()
            flash('User update successfully')
            return redirect(url_for("added_user"))
            # return render_template('update.html', form=form, name_to_update=name_to_update)

        except:
            flash('error somthing went roung plese tay agine letter')
            return render_template('update.html', form=form, name_to_update=name_to_update)

    else:
        return render_template('update.html', form=form, name_to_update=name_to_update,user_id=id)


@app.route('/user/added',methods=['GET','POST'])
def added_user():
    form=User_Form()
    user_from_database = User.query.all()
    if form.validate_on_submit():
        session['user1']=form.name.data
        user=User.query.filter_by(email=form.email.data).first()
        if user==None:
            new_user=User(user_name=form.user_name.data,name=form.name.data,email=form.email.data,password=form.password.data,favorite_color=form.favorite_color.data)
            db.session.add(new_user)
            db.session.commit()
            flash(f'user {form.name.data} has peen added')
        else:
            flash(f'user {form.name.data} is orady exists')
        form.name.data=''
        form.email.data = ''
        return redirect(url_for('added_user'))


    return render_template('added_user.html',form=form,user_from_database=user_from_database,user_session=session.get('user1'))



@app.route('/')
def index():
    first_name='jone'
    stuff='this is  bold  stuff'
    favorite_pizza=['papperoni','cheese','tumato',100,]

    return render_template('index.html',first_name=first_name,stuff=stuff,pizza=favorite_pizza)


@app.route('/user/<name>')
def user(name):

    return render_template('user.html',name=name)


@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def error_500(e):
    return render_template('500.html'),500



@app.route('/test_pw',methods=['GET','POST'])
def test_pw():
    email=None
    password=None
    pw_to_chack=None
    passed=None
    form=PasswordForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password_hash.data

        form.email.data=''
        form.password_hash.data=''
        # flash('Form Submit Successfully!')

        pw_to_chack=User.query.filter_by(email=email).first()


        passed=check_password_hash(pw_to_chack.password_hash,password)
    return render_template('test_pw.html',form=form,email=email,password=password,pw_to_chack=pw_to_chack,passed=passed)


@app.route('/name',methods=['GET','POST'])
def name():
    session['name']=None
    form=Name_Form()
    if form.validate_on_submit():
        session['name']=form.name.data
        form.name.name=''
        flash('Form Submit Successfully!')
    return render_template('name.html',form=form,name=session.get('name'))


