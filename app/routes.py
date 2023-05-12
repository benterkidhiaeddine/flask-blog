
from datetime import datetime
from flask import render_template,flash,redirect,url_for,request
from werkzeug.urls import url_parse
from flask_login import login_user,logout_user,current_user,login_required
from .models import User,Post
from . import app,db
from .forms import LoginForm,RegisterForm,EditPersonalInfoForm



@app.route("/")
@app.route("/index")
@login_required
def index():
    
    title = 'Home'
    user = current_user
    posts = current_user.followed_posts().all()
    return render_template("index.html",title = title,posts = posts, user = user)


@app.route("/login",methods=["POST","GET"])
def login():
    title = "Login"
    form = LoginForm()
    #if the user is already authenticated redirect him to the home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #if the form is valid 
    if  form.validate_on_submit():
        #query the database for the user by the user_name
        user = User.query.filter_by(username = form.username.data ).first()
        #if the user does not exist or password is incorrect flash error message and redirect to login 
        if user is None or not user.check_password(form.password.data):
            flash('User is invalid or credentials are not correct')
            return redirect(url_for('login'))
        #if the user is correct and credentials are correct login the user and remember him 
        login_user(user,remember=form.remember_me.data)
        #redirect to home page by default if there was no previous page before the redirect
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':#we check if a malicious user has set next query to a absolute url for another website, we do that by checking if the network locator of the url passed is relative , that's only the case when netloc is equal to '' 
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html",form = form, title =title )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register',methods=['POST','GET'])
def register():
    title = "register"
    if current_user.is_authenticated: # type: ignore
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data) # type: ignore
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user,remember=True)
        return redirect(url_for('index'))
    
    
    return render_template('register.html',form = form,title = title)


@app.route('/user/<username>')
@login_required
def user_profile(username):


    user = User.query.filter_by( username = username).first_or_404()
    title = f'Profile : {user.username}'
    posts =  user.posts.all()
    return render_template('profile.html',posts = posts,title =title , user = user)


#define a route that handles that editing the persons profile info
@app.route("/edit_profile",methods = [ "POST","GET"])
def edit_profile():
    form = EditPersonalInfoForm(current_user.username)
    title = "Edit profile"
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('user_profile',username = current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        
    return render_template('edit_profile.html',form = form , title = title)


@app.route('/follow/<username>')
def follow(username):
    followed_user = User.query.filter_by( username = username ).first()

    current_user.follow(followed_user)
    db.session.commit()

    return redirect(url_for('user_profile',username=username))

@app.route('/unfollow/<username>')
def unfollow(username):
    followed_user = User.query.filter_by( username = username ).first()
    current_user.unfollow(followed_user)
    db.session.commit()

    return redirect(url_for('user_profile',username=username))

#defining when the user is last seen
@app.before_request
def set_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


