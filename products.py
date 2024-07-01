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
        
    def __repr__(self):
        return '{}'.format(self.name)
    
    def __str__(self):
        return f"{self.name}\nPrice per week: {self.price_per_week}"
        
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
        return self._rental_time is None
        

        
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

class Laptop(Product):
    """ Class to represent a laptop, which is-a Product
    
    Args:
        name (str): Product's name.
        price_per_week (float, optional): Product's rental price per week.
            Defaults to 0.
    
    Attributes:
        name (str): Product's name.
        product_id (str): Unique product ID given by uuid.uuid1().
        buyable (bool): Product's status regarding purchases. Defaults to False.
    
    Class Attribute(int): 
        max_rental_time: maximum of a loan for a laptop
        
    """
    
    max_rental_time = 12
    
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
        assert rental_time <= Laptop.max_rental_time, 'Rental time must be below {} weeks'.format(Laptop.max_rental_time)
        if self.available:
            self._rental_time = rental_time
            self._rental_start = datetime.date.today()
            return True
        else:
            return False
    
    @property
    def rental_time(self):
        """int: rental duration in weeks. Can be extended."""
        return self._rental_time
    
    @rental_time.setter
    def rental_time(self, new_time):
        assert isinstance(new_time, (int, float)), "New time must be int or float"
        assert self._rental_start is not None, "The item is not rented yet"
        if self._rental_time is not None:
            assert new_time <= Laptop.max_rental_time, "You can loan laptops for a maximum of 12 months"
            assert new_time > self._rental_time, "New rental time must be greater than the current rental time"
        assert new_time > 0, 'New time must be positive'
        self._rental_time = new_time

    @classmethod    
    def display_max_rental_time(cls):
        """Displays maximum rental time for product."""
        return cls.max_rental_time
        
    @classmethod
    def from_list(cls, a_list):
        assert isinstance(a_list, list), "Given argument has to be of the type: list"
        assert len(a_list) <= 2, "Given list should have at may two entries"
        if len(a_list) == 2:
            name = a_list[0]
            price_per_week = a_list[1]
            return cls(name, price_per_week)
        elif len(a_list) == 1:
            name = a_list[0]
            return cls(name)
        else:
            return "Something went wrong sry."
    
class Phone(Product):
    """
    Contains basic attributes of a Phone. Subclass of Product.
    
    Args:
        name (str): Product's name.
        price_per_week (float): Product's rental price per week. Defaults to None.
    
    Attributes:
        name (str): Product's name.
        product_id (str): Unique product ID given by uuid.uuid1().
        buyable (bool): Product's status regarding purchases. Defaults to True.
        price_per_week (float): Product's rental price per week.
    
    """
    def __init__(self,
                 name,
                 price_per_week=0,
                 buyable = True):
        super().__init__(name, price_per_week)
        self.buyable = buyable
    
    @classmethod
    def from_dict(cls, a_dictionary):
        """Allows class creation from dict of parameters."""
        
        assert isinstance(a_dictionary, dict), "Given argument needs to be of the type: dictionary"
        assert 'name' and 'price_per_week' in a_dictionary.keys(), "Given dictionary should contain the keys name and price_per_week"
        
        return cls(name = a_dictionary.get('name'), price_per_week= a_dictionary.get("price_per_week"))