import uuid
from datetime import datetime, timedelta
from flask import Flask, make_response, request, render_template
import functools 

app = Flask(__name__)

def cookie(orignal_function):
    import uuid
    from datetime import datetime, timedelta
    from flask import Flask, make_response, request
   
    def wrapper(*args, **kwargs):
        print("this is me")
        cookie_id = 1
        # if cookie_id ==None:
        #         generate =  uuid.uuid4()
        #         max_age= datetime.strftime(datetime.utcnow() + timedelta(seconds=30), '%a ,%d-%b-%Y %H:%M %S GMT')
        #         # response = make_response( orignal_function(*args, **kwargs))
        #         # response.set_cookie("cart_id", str(generate))
        if cookie_id :
            return orignal_function(*args, **kwargs)
            
        return wrapper

def cart_id(original_function):
    #importing modules
    import uuid
    from datetime import datetime, timedelta
    from flask import  make_response, request

    @functools.wraps(original_function)
    def wrapper_function(*args, **kwargs):
        """
        cart request and verfication
        """
        cookie_id =request.cookies.get('cart_id')
        if cookie_id ==None:
                generate =  uuid.uuid4()
                max_age= datetime.strftime(datetime.utcnow() + timedelta(seconds=30), '%a ,%d-%b-%Y %H:%M %S GMT')
                response = make_response( original_function(*args, **kwargs))
                response.set_cookie("cart_id", str(generate))
                return response
        return original_function(*args, **kwargs)
        
    return wrapper_function
    



@app.route("/")
@cart_id
def home_page():
        # response = make_response("<h1>This is the HomePage</h1>")
        # response.set_cookie("cart_id","123456")
        # return response
        return "<h1> I am The Man Done!</h1>"
    
    


@app.route("/getcookie")
def GetCookie_cart_id():
    cart_id = request.cookies.get('cart_id')
    return cart_id

app.run(debug=True)