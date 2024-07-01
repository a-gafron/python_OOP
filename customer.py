import datetime
from store import RentalStore
from products import Product, Laptop, Phone

NoneType = type(None)

class Customer():
    """
    Serves as the main interface of the rental system. Stores information about customers 
    and allows interactions with store and products.
    
    Args:
        name (str): Customer name.
        store (RentalStore): Store to which customer belongs.
        current_items (list): Currently rented items. Defaults to empty list.
        
    Attributes:
        name (str): Customer name.
        store (RentalStore): Store to which customer belongs.
        
    Properties:
        invoice (float):  Outstanding amount to pay by customer for due items.
        current_items (list): Currently rented items.
        owned_items (list): Items bought from store.
        due_items (list): Rented, unpaid items after their rental period has ended.
        paid_items (list): Rented, paid items after their rental period has ended.
        invoice (float): Outstanding amount to pay by customer for rented items. Defaults to 0.0.

    """

    def __init__(self,
                 name,
                 store,
                 current_items=None):
        if isinstance(current_items, NoneType):
            current_items = []
        assert isinstance(store, RentalStore), 'Customer needs to be linked to a valid RentalStore'
        for item in current_items:
            assert isinstance(item, Product), 'Can only rent Product Objects'
        self.name = name
        self.store = store
        self._rented_items = []
        self._paid = {}
        self._owned_items = [] # for purchased items