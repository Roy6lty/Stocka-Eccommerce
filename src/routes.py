from src import app
from flask import render_template, redirect, url_for
from src.models import Item,user
from src.forms import RegisteredForm
from src import db

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
@app.route('/register', methods = ['POST','GET'])
def register_page():
    form = RegisteredForm()
    if form.validate_on_submit():
        user_to_create = user(username=form.Username.data,
                              email=form.Email_address.data,
                              password_hash=form.Password.data)
        user_to_create.create_account()
        return redirect(url_for('market_page'))
    return render_template('register.html', form=form)