from src import app
from flask import render_template, redirect, url_for, flash
from src.models import Item,user
from src.forms import RegisteredForm, LoginForm
from src import db
from flask_login import login_user, logout_user

@app.route('/home')
@app.route('/')
def home_page():

    return render_template('home.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html',items=items)

@app.route('/database')
def database_page():
    items= user.query.all()
    return render_template('database_table.html', items=items)

@app.route('/register', methods = ['POST','GET']) #Routing to registeration page
def register_page():
    form = RegisteredForm()
    if form.validate_on_submit(): #validation of data entry
        user_to_create = user(username=form.Username.data,
                              email=form.Email_address.data,
                              password_hash=form.Password.data)
        user_to_create.create_account()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error message with creating a user:{err_msg}',category='danger')

   
    return render_template('register.html', form=form)

@app.route('/login', methods = ['POST','GET'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user = user.query.filter_by(username=form.Username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.Password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match! Try again', category='danger')

    return render_template('login.html', form=form)