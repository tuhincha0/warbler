from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=6)])
    new_password_confirm = PasswordField('Confirm New Password', validators=[InputRequired(), EqualTo('new_password', message="Passwords must match.")])
    submit = SubmitField('Change Password')
