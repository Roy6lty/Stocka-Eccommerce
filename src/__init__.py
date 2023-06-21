from .extentions import db, login_manger, session, bcrypt, Message, mail
from flask import Flask, current_app as app
from .config import config



def create_app(config_name):
    app = Flask(__name__)

    #Configuration
    app.config.from_object(config[config_name])
    app.config.from_object(config['session'])
    app.config.from_object(config['mail'])
    app.config.from_object(config['upload'])



    db.init_app(app)
    login_manger.init_app(app)
    session.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from .login_app.view_login import app_login
    from .market_app.view_market import app_market
    from .user_profile.view_profile import profile
    from .product_app.view_products import app_product

    login_manger.login_view = 'app_login.login_page'
    login_manger.login_message_category = 'info'

    
    #Views
    app.register_blueprint(app_login, url_prefix = "")
    app.register_blueprint(app_market, url_prefix = "")
    app.register_blueprint(profile, url_prefix = "")
    app.register_blueprint(app_product, url_prefix = "")

    
    with app.app_context():
        db.create_all()



    return app