import uuid
from dataclasses import dataclass
from .extentions import redis_connector
import redis


@dataclass
class Shoppingcart:
    cart_id: str #unique uuid number
    cart_items: list #list of product id
    

def Cart_Id(original_function):
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


def add_to_cart(conn, cart_id:str, product_id:int):
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


def delete_item(conn, cart_id:str, product_id:str):
    """
    This Function Deletes item from cart
    cart_id: unique uuid number 
    product_id: unique product_id
    """


    count = conn.hget(cart_id, product_id)
    if count:
        conn.hdel(cart_id, product_id)
    items =conn.hgetall(cart_id)
    return items 





     


    

