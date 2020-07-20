from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, ValidationError, BooleanField, TextAreaField,SelectField
from wtforms.validators import Required,Email,EqualTo, Length
from ..models import User

class CommentForm(FlaskForm):
    comment = TextAreaField('Your comment:', validators=[Required()])
    submit = SubmitField('Comment')

class BlogForm(FlaskForm):
    # category = SelectField('Category', choices=pitch_category, validators=[Required()])
    tags = StringField('Categories:', validators=[Required()], render_kw={"placeholder": "Enter tags related to your blog(separate with commas)"})
    title = StringField('Enter Title', validators=[Required(), Length(min = 3, max = 255)])
    blog = TextAreaField('Blog:', render_kw={"placeholder": "Write blog here..."})
    submit = SubmitField('Publish Blog')