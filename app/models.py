from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import db,login
from hashlib import md5

#association table for users : followers and followed

followers = db.Table('followers',
                         db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
                         db.Column('followed_id',db.Integer,db.ForeignKey('user.id'))
)



#UserMixin has four methods necessary for the login manager : is_authenticated , is_active , is_anonymous , get_id 
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    #index =True is to make the search much faster at the expense of more memory
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    hashed_password = db.Column(db.String(128))
    posts = db.relationship("Post",backref="author",lazy ='dynamic')
    
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)

    
    #first argument is the the other side of the relationship and the second argument is the association table
    
    followed = db.relationship('User',secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref = db.backref('followers',lazy = 'dynamic'), lazy ='dynamic')

    
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)


    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    def followed_posts(self):
        
        followed_posts = Post.query.join(
            followers,(followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own_posts = Post.query.filter_by(user_id = self.id)
        return followed_posts.union(own_posts).order_by(Post.time_stamp.desc())   
    
    #def __repr__ for making debugging easier it give a clear representation of a database item when calling print on an db object
    def __repr__(self):
        return f"<User {self.username}>"
    
    #for setting up the gravatar image profile
    def avatar(self,size):
        email_md5_hash = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{email_md5_hash}?d=identicon&s={size}'
    
    
    #methods for setting and checking the passwords of users

    def set_password(self,password):
        self.hashed_password = generate_password_hash(password)
        

    def check_password(self,password):
        return check_password_hash(self.hashed_password,password)
    

    
   
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    #when the post is created of no time stamp is provided we give the moment the post was created by default (here we pass the function and not the call of the function right now)
    time_stamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Post {self.body}>"
    
#the call back function that decorates the user_loader must interact with the User model and checks if the id given as a string exists in the database 
#if not it should return None
@login.user_loader
def load_user(id):
    return User.query.get(int(id))