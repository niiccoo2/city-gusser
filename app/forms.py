from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    guess = StringField('City:', validators=[DataRequired()])
    submit = SubmitField('Guess')