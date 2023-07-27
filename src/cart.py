import uuid
from dataclasses import dataclass
from .extentions import redis_connector
import redis
from typing import Type


class Shoppingcart:
     pass

def CartId(original_function):
    #importing modules
    import uuid, functools
    from datetime import datetime, timedelta
    from flask import  make_response, request

    @functools.wraps(original_function)
    def wrapper_function(*args, **kwargs):
        """
        cart request and verfication
        """
        cookie_id =request.cookies.get('cart_id') #cookie_id
        if cookie_id ==None: 
                generate =  uuid.uuid4()
                max_age= datetime.strftime(datetime.utcnow() + timedelta(seconds=30), '%a ,%d-%b-%Y %H:%M %S GMT')
                response = make_response( original_function(*args, **kwargs))
                response.set_cookie("cart_id", str(generate))
                return response
        return original_function(*args, **kwargs)
        
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
        conn.hsetnx(cart_id, product_id, 1) #add item to cart

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





     


    

