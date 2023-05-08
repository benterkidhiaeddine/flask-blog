from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,Length
from .models import User


class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")

class RegisterForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    confirm_password = PasswordField('confirm your password',validators=[DataRequired(),EqualTo('password',"passwords don't match")])
    submit  =SubmitField("Register")

    #define functions to raise an error when a user name or an email is already in use

    def validate_username(self,given_username):
        user = User.query.filter_by(username = given_username.data).first()
        if user is not None:
            raise ValidationError('Pleas user a different username.')

    def validate_email(self,given_email):
        user = User.query.filter_by(email = given_email.data).first()
        if user is not None:
            raise ValidationError('Pleas use a different email address')
        

class EditPersonalInfoForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    about_me = TextAreaField('About me',validators=[Length(min = 0, max =140)])
    submit = SubmitField('Submit')

    #here we are going to pass the current_user username
    def __init__(self,original_username,*args,**kwargs):
        super(EditPersonalInfoForm,self).__init__(*args,**kwargs)
        self.original_username = original_username

    def validate_username(self,given_username):
        if given_username.data != self.original_username:
            user = User.query.filter_by(username = given_username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
