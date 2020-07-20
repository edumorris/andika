from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    comments = db.relationship('Comment', backref = 'user_comments', lazy = "dynamic")
    pitchs = db.relationship('Blog', backref = 'user_blog', lazy = "dynamic")
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__="blogs"
    blog_id = db.Column(db.Integer, primary_key = True)
    blog_title = db.Column(db.String(255))
    blog = db.Column(db.String())
    tags = db.Column(db.String(1000))
    upvotes = db.Column(db.Integer)
    downvote = db.Column(db.Integer)
    submitted_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Comment', backref = 'blog_comment', lazy = "dynamic")

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

class Comment(db.Model):
    __tablename__="comments"
    comm_id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String(10000))
    for_blog = db.Column(db.Integer, db.ForeignKey("blogs.blog_id"))
    submitted_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    submission_date = db.Column(db.DateTime,default=datetime.utcnow)

class Quotes():
    def __init__(self, id, author, quote, link):
        self.id = id
        self.author = author
        self.quote = quote
        self.link = link