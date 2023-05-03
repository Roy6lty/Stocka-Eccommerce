from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from src.models import user

class RegisteredForm(FlaskForm):

    def validate_Username(self, username_to_check):
        User = user.query.filter_by(username=username_to_check.data).first()
        if User:
            raise ValidationError('Username already exis!t')
        
        
    def validate_Email_address(self, email_address_to_check):
        User = user.query.filter_by(email=email_address_to_check.data).first()
        if User:
            raise ValidationError('Email Address already exis!t')
        
    
    Username = StringField(label= 'Username', validators=[Length(min=2, max=30),DataRequired()])
    Email_address = StringField(label= 'Email Address',validators=[Email(), DataRequired()])
    Password = PasswordField(label= 'Password',validators=[Length(min=6),DataRequired()])
    Confirm_Password = PasswordField(label= 'Confirm Password',validators = [EqualTo('Password'), DataRequired()])
    Create_Account = SubmitField(label = 'Create Account')
    


