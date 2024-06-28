import uuid
import datetime
NoneType = type(None)


class Product():
    """
    Contains basic attributes and properties of a product.
    
    Args:
        name (str): Product's name.
        price_per_week (float, optional): Product's rental price per week.
            Defaults to 0.
    
    Attributes:
        name (str): Product's name.
        product_id (str): Unique product ID given by uuid.uuid1().
        buyable (bool): Product's status regarding purchases. Defaults to False.
    
    """

    def __init__(self, 
                 name,
                 price_per_week=0):
        #assert statements to check types
        assert isinstance(name, str), 'name must be string'
        assert isinstance(price_per_week, (int, float, NoneType)), 'price_per_week must be int, float or None'
        
        self.name = name
        self.product_id = str(uuid.uuid1())
        self.buyable = False
        self._price_per_week = price_per_week
        self._rental_time = None
        self._rental_start = None
        

    