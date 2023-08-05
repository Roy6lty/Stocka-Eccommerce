import jwt
from flask import current_app as app
from datetime import time, datetime, timezone, timedelta
from flask import jsonify
from starlette import status
from PIL import Image
import secrets
import os
from celery import Celery, Task
from flask import Flask
from blinker import signal


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app

    return celery_app

    

def tokens()-> str:
    """
    Generate unique 8 bit identifier
    """
    random_hex = secrets.token_hex(8)
    return random_hex

def save_picture(picture, save_path:str, output_size:tuple)-> str:
    """
   picture: Uploaded image
   save_path: save location
   output_size: image output size
   """
    random_hex = tokens() #generating Hex
    _, f_ext = os.path.splitext(picture.filename) #spliting filename and extention
    pic_fn  =random_hex + f_ext #appending new File name
    picture_path = os.path.join(app.root_path, save_path, pic_fn) 
    output_size = output_size
    img =Image.open(picture)
    img.thumbnail(output_size)

    img.save(picture_path)  #saving picture locally
    return pic_fn
   

class password_reset:

    @staticmethod
    def token_encoder(*args, **kwargs):
        token = jwt.encode({
                    'expiration': str(datetime.now(tz=timezone.utc) + timedelta(seconds = 300))
                    **kwargs
                },
                app.config['SECRET_KEY']
                )
        return token
    
    @staticmethod
    def token_decoder(token):
        payload = jwt.decode(
            token,
            key = app.config['SECRET_KEY']
        )

        return jsonify(payload, status = status.HTTP_200_OK )


    

