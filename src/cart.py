import uuid
from dataclasses import dataclass

@dataclass
class Shoppingcart:
    cart_id: uuid
    cart_items: dict
    

def cart_id(original_function):
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



    

