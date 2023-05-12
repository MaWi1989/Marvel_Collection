from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, TextAreaField, IntegerField, BooleanField, Form, FormField
from wtforms.validators import DataRequired, Email


class UserSignupForm(FlaskForm):
    first_name = StringField('First Name', validators= [DataRequired()])
    last_name = StringField('Last Name', validators= [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    username = StringField('Username', validators= [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')



class UserLoginForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')


class MarvelCharacterForm(FlaskForm):
    name = StringField('Name') 
    description = StringField('Description')
    series = StringField('Series')
    powers = StringField('Super Powers')
    comics_appeared_in = IntegerField('Comics Appeared In')
    first_appeared_in = StringField('First Appeared In')
    year_introduced = IntegerField('Year Introduced')
    submit_button = SubmitField('Submit')

