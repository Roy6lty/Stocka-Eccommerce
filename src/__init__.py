from .extentions import (db, login_manger, session, bcrypt, 
                                Message, mail, redis_connector, mongo, client, current_user)
from flask import Flask, g, request, current_app as app
from src.config import config, BaseConfig
from .models import RoleUser
from .MongoCRUD import StockaProducts, Struct
from redis.exceptions import DataError
from .utils import  celery_init_app





def create_app(config_name:str):
    app = Flask(__name__)

    #Configuration
    app.config.from_object(config[config_name])
    app.config.from_object(config['session'])
    app.config.from_object(config['mail'])
    app.config.from_object(config['upload'])
    app.config.from_object(config['mongo'])
    app.config.from_object(config['secret'])
    app.config['SQLALCHEMY_DATABASE_URI'] = BaseConfig.SQLALCHEMY_DATABASE_URI
    print(BaseConfig.SQLALCHEMY_DATABASE_URI)
   

    app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        ),
    )

    celery_app = celery_init_app(app)
    

    #intilzation with flask app instance
    db.init_app(app) #sqlite database
    login_manger.init_app(app) 
    session.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app) 
    mongo.init_app(app) #mongodb

    from .login_app.view_login import app_login
    from .market_app.view_market import app_market
    from .user_profile.view_profile import profile
    from .product_app.view_products import app_product
    from .merchant_app.view_merchant import app_merchant
    from .checkout_app.view_checkout import app_checkout

    login_manger.login_view = 'app_login.login_page'
    login_manger.login_message_category = 'info'

    
    #Views
    app.register_blueprint(app_login, url_prefix = "")
    app.register_blueprint(app_market, url_prefix = "")
    app.register_blueprint(profile, url_prefix = "")
    app.register_blueprint(app_product, url_prefix = "/shopping")
    app.register_blueprint(app_merchant, url_prefix = "/merchantstocka")
    app.register_blueprint(app_checkout, url_prefix="/checkout")
  

    @app.context_processor
    def cart_loader()-> dict:
        from bson.objectid import ObjectId
        """
        **/ This function return the cart item for a user in a context
        /
        """
        if current_user.is_authenticated:
            cart_id = current_user.cart_id
        else:
            cart_id = request.cookies.get('cart_id')
        try:
            cart = redis_connector.hgetall(cart_id)
        except DataError:     #redis returns Nonetype obj
            cart = dict()     #intialixe empty dict

        product_id = [ObjectId(key) for key in cart.keys()] #list of mongo object id
        query = {"_id":{"$in" : product_id}}
        items = zip(StockaProducts.find(query), #returns a generator of mongodb obj
                    (cart.values())) # returns generator product quantity 
        return dict(cart = items)
    

    @app.context_processor
    def page_loader()-> dict:
        """_summary_
        This function returns the previous view function for a user
        Returns:str(endpoint function)
            _type_: _description_
        """
        name = 'name' #declaring variable
        endpoint, path = app.view_functions.get(request.url_rule.endpoint, None), app.view_functions
        value =  {name :i for i in path if path[i] == endpoint} #returns matching endpoint
        value['name'] #returns name of endpoint function
        
        return dict(page_function = value['name']) 
        

   
    with app.app_context():
        db.create_all()
        RoleUser.db_load(app, db)



    return app, celery_app