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
        
    @property
    def invoice(self):
        """float: Outstanding amount to pay by customer for due items."""
        return sum([item.rental_time * item.price_per_week for item in self.due_items])
    
    @property
    def current_items(self):
        return [item for item in self._rented_items if item.rental_end > datetime.date.today()]
    
    @property
    def due_items(self):
        return [item for item in self._rented_items
                if item.rental_end <= datetime.date.today()
                and not self._paid[item.product_id]]
    
    @property
    def paid_items(self):
        return [item for item in self._rented_items
                if item.rental_end <= datetime.date.today()
                and self._paid[item.product_id]]
    
    @property
    def owned_items(self):
        return self._owned_items
    
    def pay_invoice(self, amount_paid):
        """Pay invoice and reset it to 0.0. Removes payed for items from current_items.
        
        Args:
            amount_paid (float): Amount to pay to settle invoice.

        """

        assert isinstance(amount_paid, (int, float)), 'amount_paid must be int or float'
        assert amount_paid > 0, 'amount_paid must be positive'
        assert self.invoice == amount_paid, 'Whole bill must be paid, no partial payments possible'

        # delete old items
        for item in self.due_items:
            self._paid[item.product_id] = True