from flask import render_template, request, redirect, url_for, abort, flash, send_from_directory
from . import main
from ..models import Comment, User, Blog, Quotes
from ..requests import get_quote
from flask_login import login_required
from .forms import BlogForm, CommentForm
from .. import db
import os
import markdown2
from sqlalchemy import desc

# Main page
@main.route('/')
def index():
    '''
    Homepage
    '''

    blog = Blog.query.all()

    blog_latest = Blog.query.order_by(desc(Blog.blog_id)).first() # Most Recent Blogs

    latest_blogs = Blog.query.order_by(desc(Blog.blog_id)).all()

    # Getting random quote
    random_quote = get_quote()

    title = 'Andika'

    return render_template('index.html', blog = blog, blog_latest = blog_latest, latest_blogs = latest_blogs, quote_store = random_quote, title = title)

'''
@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
'''



@main.route('/blog/comment/new/<user>/<int:id>', methods = ['GET', 'POST'])
@login_required
def comment(id, user):
    form = CommentForm()

    blog_content = Blog.query.filter_by(blog_id = id).first()
    format_content = markdown2.markdown(blog_content.blog, extras=["code-friendly", "fenced-code-blocks"])

    comments = Comment.query.filter_by(for_blog = id).all()

    title = blog_content.blog_title

    if form.validate_on_submit():
        users_comment = Comment(comment = form.comment.data, for_blog = id, submitted_by = user)

        db.session.add(users_comment)
        db.session.commit()

        flash("Comment added successfully!")
        return redirect(url_for('main.comment', id = blog_content.blog_id, user = user, title = title))
    
    return render_template('comment.html', comment_form = form, blog_content = blog_content, comments = comments, format_content = format_content)

@main.route('/blog/new/<uname>/', methods = ['GET', 'POST'])
@login_required
def new_blog(uname):
    form = BlogForm()

    if uname is None:
        return redirect(url_for('auth.login'))

    if form.validate_on_submit():
        user = User.query.filter_by(username = uname).first()

        # Submitting the data
        blog_data = Blog(blog_title = form.title.data, blog = form.blog.data, tags = form.tags.data, upvotes  = 0, downvote = 0, submitted_by = user.id)

        blog_data.save_blog()

        return redirect(url_for('main.index'))

    return render_template('blog.html', uname=uname, blog_form = form)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = user.id

    # Getting blog by users
    # user_id = User.query.filter_by(id = user.id).first()
    blog_data = Blog.query.filter_by(submitted_by = user_id).all()

    if user is None:
        abort(404)
        
    
    return render_template("profile/profile.html", user = user, blog_data = blog_data)

@main.route('/blog/<int:id>/upvote', methods = ['GET', 'POST'])
def upvote(id):
    blog = Blog.query.filter_by(blog_id = id).first()

    upvote = blog.upvotes
    new_upvotes = upvote + 1

    new_blog = Blog.query.filter_by(blog_id = id).update({"upvotes": new_upvotes})
    db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/blog/<int:id>/downvote', methods = ['GET', 'POST'])
def downvote(id):
    blog = Blog.query.filter_by(blog_id = id).first()

    downvote = blog.downvote
    new_downvote = downvote + 1

    new_blog = Blog.query.filter_by(blog_id = id).update({"downvote": new_downvote})
    db.session.commit()

    return redirect(url_for('main.index'))