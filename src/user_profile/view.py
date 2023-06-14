from ..extentions import db
from flask import current_app as app
from ..extentions import db, Message, mail
from flask import render_template, redirect, url_for, flash, request,session, Blueprint
from ..models import user
from ..forms import AccountUpdate
from flask_login import login_user, logout_user, login_required, current_user
import datetime 
import jwt
import socket
socket.setdefaulttimeout(10)
import os
import secrets
#from ..logger import logging

profile = Blueprint('profile', __name__, static_folder="static",static_url_path='src/user_profile/static', template_folder="user_templates")


def save_picture(form_picture):
    '''
    saving picture name with a 8 bit random_hex
    '''
    random_hex = secrets.token_hex(8) #generating Hex
    _, f_ext = os.path.splitext(form_picture.filename) #spliting filename and extention
    pic_fn  =random_hex + f_ext #appending new File name
    print(app.config['UPLOAD_FOLDER'], app.root_path)
    picture_path = os.path.join(app.root_path, 'user_profile/static/profile_pic', pic_fn) 
    print(picture_path)
    form_picture.save(picture_path) #saving picture locally
    return pic_fn


@profile.route('/account', methods = ['POST','GET'])
@login_required
def account():
    form = AccountUpdate()
   
    if request.method == 'POST' and form.validate():
        if form.Picture.data:
            picture_file = save_picture(form.Picture.data) # saving profile picture
            current_user.image_file = picture_file # updating profile pic

        current_user.username = form.Username.data #updating username
        current_user.email = form.Email_address.data #updating email
        db.session.commit() #saving changes
        flash("Your account has been updated", category = 'success')
        return redirect(url_for('profile.account'))
    
    elif request.method == 'GET' :
        form.Username.data = current_user.username
        form.Email_address.data = current_user.email
      
    if form.errors != {}:
        for err_msg in form.errors.items():
            print(form.errors.values())
            flash(f'There was an error message with creating a user:{err_msg}',category='danger')
        
    image_file = url_for('.static', filename = 'profile_pic/' + current_user.image_file) 
    return render_template('account.html', title = "Account", image_file = image_file, form = form)
