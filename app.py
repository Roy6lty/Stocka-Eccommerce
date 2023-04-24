from flask import Flask, render_template
app = Flask(__name__)

@app.route('/home')
@app.route('/')
def home_page():

    return render_template('home.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/market')
def market_page():
    items = [
        {'id':1, 'name':'Phone','barcode':'893212299897','price':500},
        {'id':2, 'name':'Laptop','barcode':'123661234355','price':1000},
        {'id':3, 'name':'Keyboard','barcode':'2345336643244','price':300}
             ]
    return render_template('market.html',items=items)