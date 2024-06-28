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
        
    @property
    def price_per_week(self):
        """int, float: Product's rental price per week."""
        return self._price_per_week
    
    @price_per_week.setter
    def price_per_week(self, new_price):
        assert isinstance(new_price, (int, float)), 'New price must be int or float'
        assert new_price > 0, 'New price must be positive'
        self._price_per_week = new_price
        
    @property
    def rental_start(self):
        """datetime.date: only set by rent()"""
        return self._rental_start
    
    @property
    def rental_time(self):
        """int: rental duration in weeks"""
        return self._rental_time
    
    @rental_time.setter
    def rental_time(self, new_time):
        assert isinstance(new_time, (int, float)), "New time must be int or float"
        assert self._rental_start is not None, "The item is not rented yet"
        if self._rental_time is not None:
            assert new_time > self._rental_time, "New rental time must be greater than the current rental time"
        assert new_time > 0, 'New time must be positive'
        self._rental_time = new_time
        
    @property
    def rental_end(self):
        """datetime.date: returning the date when loan ends"""
        if self._rental_start is None or self._rental_time is None:
            return None
        return (self.rental_start + datetime.timedelta(weeks=self.rental_time))
    
    @property
    def available(self):
        """bool: available == True"""
        if self._rental_time == NoneType:
            return True
        else:
            return False
        

        
    def rent(self, rental_time):
        """
        Rent product for given rental time.
        
        Args:
            rental_time (int): Time to rent the product in weeks.
                Must be strictly positive.
                
        Returns:
            True if Product is available, False otherwise.
        """
        assert isinstance(rental_time, int), 'rental_time must be int'
        assert rental_time > 0, 'rental_time must be positive'
        if self.available:
            self._rental_time = rental_time
            self._rental_start = datetime.date.today()
            return True
        else:
            return False

    def product_description(self):
        print('Product: {}\nPrice per week: {}'.format(self.name, self.price_per_week))
    