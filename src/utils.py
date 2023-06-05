import jwt
from src import app
from datetime import time, datetime, timezone, timedelta
from flask import jsonify
from starlette import status


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


    

