from .extentions import client
#create collections


#defining Colllection
StockaProducts = client.stocka.products
StockaShops = client.stockashop
StockaReviews = client.stocka.collection
StockaCategories = client.stocka.categories

class Struct(object):
    """
    This class deserializes json in dictobj
    """
    def __init__(self, data):
        for name, value in data.items():
            setattr(self, name, self._wrap(value))
    def _wrap(self, value):
        if isinstance(value, (tuple, list, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return Struct(value) if isinstance(value, dict) else value 
        
    @staticmethod
    def submit(value):
        if isinstance(value, list):
            return list(map(lambda obj: Struct(obj), value))
        return Struct(value)

