from ..extentions import redis_connector
from flask import request, Blueprint, current_app as app
from ..MongoCRUD import StockaProducts, Struct
from redis.exceptions import DataError


