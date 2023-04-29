from src import app
from flask import render_template
from src.models import Item,user

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