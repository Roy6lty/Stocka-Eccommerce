from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, file_required
from flask_login import current_user
from flask import flash
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from .models import User

class RegisteredForm(FlaskForm):

    def validate_Username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist!')
        
        
    def validate_Email_address(self, email_address_to_check):
        user = User.query.filter_by(email=email_address_to_check.data).first()
        if user:
            raise ValidationError('Email Address already exist!')
        
    
    Username = StringField(label= 'Username', validators=[Length(min=2, max=30),DataRequired()])
    Email_address = StringField(label= 'Email Address',validators=[Email(), DataRequired()])
    Password = PasswordField(label= 'Password',validators=[Length(min=6),DataRequired()])
    Confirm_Password = PasswordField(label= 'Confirm Password',validators = [EqualTo('Password'), DataRequired()])
    Create_Account = SubmitField(label = 'Create Account')
    
class LoginForm(FlaskForm):
    def validate_Username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user == None:
            raise ValidationError("Username doesn't exist")
        
    Username = StringField(label= 'Username', validators=[DataRequired()])
    Password = PasswordField(label= 'Password',validators=[DataRequired()])
    Login = SubmitField(label = 'Sign in')

class Resetpasswordform(FlaskForm):

    def validate_Email_address(self, email_address_to_check):
        user = User.query.filter_by(email=email_address_to_check.data).first()
        if user is None:
            raise ValidationError('Email Address Does Not  exist!')

    Email_address = StringField(label= 'Email Address',validators=[Email(), DataRequired()])
    Reset = SubmitField(label = 'Sumit')

class verify_Resetpasswordform(FlaskForm):
    
    Password = PasswordField(label= 'Password',validators=[Length(min=6),DataRequired()])
    Verify_Password = PasswordField(label = 'Sumit', validators = [EqualTo('Password'), DataRequired()])

    submit = SubmitField(label = 'Sumit')


    
class Sellitemform(FlaskForm):
    submit = SubmitField(label= 'Sell')

class AccountUpdate(FlaskForm):

    def validate_Username(self, Username_to_check):
        if Username_to_check.data != current_user.username:
            user = User.query.filter_by(username=Username_to_check.data).first()
            if user:
                raise ValidationError('Username already exist!')
        
        
    def validate_Email_address(self, Email_address_to_check):
        if Email_address_to_check.data != current_user.email:
            email = User.query.filter_by(email=Email_address_to_check.data).first()
            if email:
                raise ValidationError('Email Address already exist!')
         
    Username = StringField(label= 'Username', validators=[Length(min=2, max=30),DataRequired()])
    Email_address = StringField(label= 'Email Address',validators=[Email(), DataRequired()])
    Mobile_number = StringField(label = 'phone')
    Address = StringField(label= 'Address')
    State = StringField(label= 'state')
    Country =StringField(label= 'country')
    Picture = FileField("Upadate Profile Picture", validators =[FileAllowed(['jpg','png', 'jpeg'])])
    Update = SubmitField(label = 'Save Profile')
    Procced = SubmitField(label = 'Procced to checkout')

class Add_product(FlaskForm):

    # def validate_Price(self, Price_to_check):
    #     if (type(Price_to_check.data) == int) or (type(Price_to_check.data) == float):
    #         float(Price_to_check.data)
    #     raise ValidationError('Type in Proper Price')
    
    Name = StringField(label= 'Product Name', validators=[Length(min=2, max=20),DataRequired()])
    Price = StringField(label= 'Product Price', validators=[Length(min=2),DataRequired()])
    Barcode = StringField(label= 'Barcode')
    Stock = StringField(label= 'Stock', validators=[DataRequired()])
    Description = TextAreaField(label= 'Description', validators=[Length(min=10),DataRequired()])
    Picture = FileField("Product image", validators =[FileAllowed(['jpeg','jpg','png', 'webp']),DataRequired()])
    Update = SubmitField(label = 'Update')
    Submit = SubmitField(label = 'Add Product')

class Comments(FlaskForm):
    Description = TextAreaField(label= 'Description', validators=[Length(min=10)])
    Submit = SubmitField(label = 'Post')
    Addtocart = SubmitField(label= 'ADD TO CART')
   
class AddToCart(FlaskForm):
    
    Submit = SubmitField(label= 'ADD TO CART')