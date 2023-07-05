from ..extentions import db, Message, mail
from flask import render_template, redirect, url_for, flash, request,session, Blueprint
from ..models import user
from ..forms import RegisteredForm, LoginForm, Resetpasswordform, verify_Resetpasswordform
from flask_login import login_user, logout_user, login_required, current_user
from ..cart import Shoppingcart, SetCookie_cart_id, GetCookie_cart_id
import datetime 
import jwt
import socket
socket.setdefaulttimeout(10)

#from ..logger import logging




app_login = Blueprint('app_login', __name__, static_folder="static",static_url_path='login_app/static', template_folder="login_templates")



@app_login.route('/home')
@app_login.route('/')
def home_page():
    if not session.get('name'):
        cookie_id = GetCookie_cart_id()
        if cookie_id is None:
            cookie_id = SetCookie_cart_id(render_template('home.html'))
            return cookie_id
        return render_template('home.html')
        
    return redirect(url_for('app_market.market_page' ,cookie_id = cookie_id))

@app_login.route('/login', methods = ["POST","GET"])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user = user.query.filter_by(username=form.Username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.Password.data):
            login_user(attempted_user)
            session['name'] = attempted_user #setting session-name to username
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            #logging.info(f'username{attempted_user}')
            return redirect(url_for('app_market.market_page'))
        else:
            flash('Username and password do not match! Try again', category='danger')

    return render_template('login.html', form=form)



@app_login.route('/register', methods = ['POST','GET']) #Routing to registeration page
def register_page():
    form = RegisteredForm()
    if form.validate_on_submit(): #validation of data entry
            #logging.info(form.Email_address.data)
            user_to_create = user(username=form.Username.data, #db session object created
                                email=form.Email_address.data,
                                password_hash=form.Password.data)
            

            user_to_create.create_account() # db session Expire

            attempted_user = user.query.filter_by(username=form.Username.data).first() #db session object created
            login_user(attempted_user)
            session['name'] = attempted_user #User_session
            flash(f'Congratulations {attempted_user.username}! You have successfully created your account', category='success')
            return redirect(url_for('app_market.market_page'))
     
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error message with creating a user:{err_msg}',category='danger')

   
    return render_template('register.html', form=form)



@app_login.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('name', default='None')
    flash('You have successfully been logged out', category= 'info')
    return redirect(url_for('app_login.home_page'))


def send_rest_email(user):
    token = user.token_encoder(user_id = user.id)
    print(token, user.id, user.email)
    msg = Message('Password Reset Request', sender = 'noreply@flask_app.com', recipients = [user.email] )
    msg_body = f''' To Reset your password click the button Below
    {url_for("app_login.password_reset_token", token=token, _external = True)}
    if you did not make this request please ignore
    '''
    mail.send(msg)
    

@app_login.route('/reset', methods = ["GET", "POST"])
def resetpassword_page():
    form=Resetpasswordform()
    if request.method == "POST":
        attempted_user = user.query.filter_by(email=form.Email_address.data).first()
        if attempted_user:
            send_rest_email(attempted_user)
            flash('Email has been sent to with instructions to reset your password', category= 'info')
        else:
            flash('Email does not exist! Try again', category='warning')

    return render_template('resetpassword.html', form=form)



@app_login.route('reset_password/<token>', methods = ["GET","POST"])
def password_reset_token(token):
    form  = verify_Resetpasswordform()
    user_reset =  user.token_decoder()
    if user_reset is None:
        flash('That is a Expired or invaild Token',category= 'warning')
        return redirect(url_for('app_login.resetpassword_page'))
    if form.vaildate_on_submit:
        user.password = form.Password.data
        db.session.commit()
        flash('Your Password has been updated ', category='success')
        return redirect('app_login.login')
    

    return render_template('verify_password.html', form = form)

