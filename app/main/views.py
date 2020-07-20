from flask import render_template, request, redirect, url_for, abort, flash, send_from_directory
from . import main
from ..models import Comment, User, Blog, Quotes
from ..requests import get_quote
from flask_login import login_required
from .forms import BlogForm, CommentForm
from .. import db
import os

# Main page
@main.route('/')
def index():
    '''
    Homepage
    '''

    blog = Blog.query.all()

    # Getting random quote
    random_quote = get_quote()

    title = 'Andika'

    return render_template('index.html', blog = blog, quote_store = random_quote, title = title)

'''
@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
'''



@main.route('/pitch/comment/new/<user>/<int:id>', methods = ['GET', 'POST'])
@login_required
def comment(id, user):
    form = CommentForm()

    pitch_content = Pitch.query.filter_by(pitch_id = id).first()

    comments = Comment.query.filter_by(for_pitch = id).all()

    if form.validate_on_submit():
        users_comment = Comment(comment = form.comment.data, for_pitch = id, submitted_by = user)

        db.session.add(users_comment)
        db.session.commit()

        flash("Comment added successfully!")
        return redirect(url_for('main.comment', id = pitch_content.pitch_id, user = user))
    
    return render_template('comment.html', comment_form = form, pitch_content = pitch_content, comments = comments)

@main.route('/pitch/<uname>/new/', methods = ['GET', 'POST'])
@login_required
def new_blog(uname):
    form = BlogForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = uname).first()

        # Submitting the data
        pitch_data = Pitch(pitch = form.pitch.data, category = form.category.data, upvotes  = 0, downvote = 0, submitted_by = user.id)

        db.session.add(pitch_data)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('pitch.html', uname=uname, pitch_form = form)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = user.id

    # Getting pitch by users
    # user_id = User.query.filter_by(id = user.id).first()
    pitch_data = Pitch.query.filter_by(submitted_by = user_id).all()

    if user is None:
        abort(404)
        
    
    return render_template("profile/profile.html", user = user, pitch_data = pitch_data)

@main.route('/pitch/<int:id>/upvote', methods = ['GET', 'POST'])
def upvote(id):
    pitch = Pitch.query.filter_by(pitch_id = id).first()

    upvote = pitch.upvotes
    new_upvotes = upvote + 1

    new_pitch = Pitch.query.filter_by(pitch_id = id).update({"upvotes": new_upvotes})
    db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/pitch/<int:id>/downvote', methods = ['GET', 'POST'])
def downvote(id):
    pitch = Pitch.query.filter_by(pitch_id = id).first()

    downvote = pitch.downvote
    new_downvote = downvote + 1

    new_pitch = Pitch.query.filter_by(pitch_id = id).update({"downvote": new_downvote})
    db.session.commit()

    return redirect(url_for('main.index'))