from ..extentions import db
from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request, Blueprint
from ..forms import AccountUpdate
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image
from ..utils import save_picture
import socket
import os
import secrets
socket.setdefaulttimeout(10)

#from ..logger import logging

profile = Blueprint('profile', __name__, static_folder="static",static_url_path='src/user_profile/static', template_folder="user_templates")


# def save_picture(form_picture):
#     '''
#     saving picture name with a 8 bit random_hex
#     '''
#     random_hex = secrets.token_hex(8) #generating Hex
#     _, f_ext = os.path.splitext(form_picture.filename) #spliting filename and extention
#     pic_fn  =random_hex + f_ext #appending new File name
#     picture_path = os.path.join(app.root_path, 'user_profile/static/profile_pic', pic_fn) 
#     output_size =(125, 125)
#     img =Image.open(form_picture)
#     img.thumbnail(output_size)

#     img.save(picture_path)  #saving picture locally
#     return pic_fn


@profile.route('/account', methods = ['POST','GET'])
@login_required
def account():
    form = AccountUpdate()
    save_path =  'user_profile/static/profile_pic'
    output_size = (125, 125)
   
    if request.method == 'POST' and form.validate():
        if form.Picture.data:
            picture_file = save_picture(form.Picture.data, save_path, output_size) # saving profile picture
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
            flash(f':{err_msg}',category='danger')
        
    image_file = url_for('.static', filename = 'profile_pic/' + current_user.image_file) 
    return render_template('account.html', title = "Account", image_file = image_file, form = form)
