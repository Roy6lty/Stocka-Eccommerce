import uuid
from dataclasses import dataclass
from .extentions import redis_connector
from redis.exceptions import DataError 
from typing import Type
from .MongoCRUD import StockaProducts
from flask import request
from flask_login import current_user
import uuid, functools
from datetime import datetime, timedelta
from flask import  make_response, request

class Shoppingcart:
     pass

def cart_authenticator():
    """_This function verify user login status and load the user cart into 
    current_user.catr_id while deleting the old id from db
    """
    annymous_cart_id = request.cookies.get('cart_id') #possible values 1,0

    if  (current_user.is_authenticated) and (annymous_cart_id != current_user.cart_id):
        cart = redis_connector.hgetall(annymous_cart_id)
        try:
           redis_connector.hset(current_user.cart_id, mapping=cart) #inserting into database
        except DataError:  pass  
             
        





def CartId(original_function):
    #importing module

    @functools.wraps(original_function)
    def wrapper_function(*args, **kwargs):
        """
        cart request and verfication
        """
        cart_authenticator() #merging carts

        cookie_id =request.cookies.get('cart_id') #cookie_id
        if current_user.is_authenticated:
            response = make_response( original_function(*args, **kwargs))
            response.set_cookie("cart_id",current_user.cart_id)
            return response

        elif cookie_id ==None: 
                generate =  uuid.uuid4()
                max_age= datetime.strftime(datetime.utcnow() + timedelta(seconds=30), '%a ,%d-%b-%Y %H:%M %S GMT')
                response = make_response( original_function(*args, **kwargs))
                response.set_cookie("cart_id", str(generate))
                return response
        return original_function(*args, **kwargs)
        
    return wrapper_function

def DeleteCartId(original_function):
    @functools.wraps(original_function)
    def wrapper_function(*args, **kwargs):
        """
        Delete cart_id cookies on the user browser
        """
        response = make_response( original_function(*args, **kwargs))
        response.set_cookie("cart_id",max_age=0)
        return response
        
        
    return wrapper_function



def AddItem(conn:Type[redis_connector], cart_id:str, product_id:int)-> dict:
    """
    This function add product_id cart(redisdatabase)
    conn: redis connector,
    cart_id: unique cart id
    producct_id: unique product id
    """

    count = conn.hget(cart_id, product_id)
    if count is None: #if item is not in cart
        conn.hsetnx(cart_id, product_id, 1) #add item to cart, qunatity 1

    else: conn.hincrby( cart_id, product_id, 1) #increase quantity by 1

    items = conn.hgetall(cart_id) # get all items in cart
    return items


def DeleteItem(conn:Type[redis_connector], cart_id:str, product_id:str)-> dict:
    """
    This Function Deletes item from cart
    cart_id: unique uuid number 
    product_id: unique product_id
    """


    count = conn.hget(cart_id, product_id) # query  redis database for item
    if count:
        conn.hdel(cart_id, product_id) #deleting item
    items =conn.hgetall(cart_id) #returning new dict object from redis
    return items 

def RetrieveCart():
    from bson.objectid import ObjectId
    """
    **/ This function return the cart item for a user in a context
    /
    """
    cart_id = current_user.cart_id
    try:
        cart = redis_connector.hgetall(cart_id)
    except DataError:     #redis returns Nonetype obj
        cart = dict()     #intialixe empty dict

    product_id = [ObjectId(key) for key in cart.keys()] #list of mongo object id
    query = {"_id":{"$in" : product_id}}
    items = zip((StockaProducts.find(query)), #returns a generator of mongodb obj
                (cart.values())) # returns generator product quantity 
    return items


     


    

