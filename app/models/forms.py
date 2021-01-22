from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, BooleanField, TextAreaField
# from app.utils.forms import MultiCheckboxField


class BookForm(FlaskForm):
    query = TextAreaField('Query')


