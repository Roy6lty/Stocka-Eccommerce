from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import Length, Email, Equalto, DataRequired

class RegisteredForm(FlaskForm):
    Username = StringField(label= 'Username', validators=[Length(min=2, max=30),DataRequired])
    Email_address = StringField(label= 'Email Address',validators=[Email, DataRequired])
    Password = PasswordField(label= 'Password', validators=[Length(min=6), DataRequired])
    Confirm_Password = PasswordField(label= 'Confirm Password',validators=[Equalto(Password)])
    Create_Account = SubmitField(label = 'Create Account')
    


