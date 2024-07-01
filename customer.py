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
    
    def __repr__(self):
        return 'Customer: {}, {} items rented.'.format(self.name, len(self.current_items))
    
    def __str__(self):
        """Provide a user-friendly string representation of the Customer object."""
        owned_items_str = ', '.join(item.name for item in self.owned_items)
        rented_items_str = ', '.join(item.name for item in self.current_items)
        due_items_str = ', '.join(item.name for item in self.due_items)
        
        return (f"{self.name}\n"
                f"Owned items: [{owned_items_str}]\n"
                f"Rented items: [{rented_items_str}]\n"
                f"Due items: [{due_items_str}]\n"
                f"Amount payable: {self.invoice}")
        
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
            
    def rent(self, item_name, rental_time):
        """Rent item for specific amount of time.
        
        Args:
            item_name (str): Item name as given by Product.__repr__().
            rental_time (int): Rental time in weeks.
        
        Raises:
            AssertionError: If item_name not in self.store.products.

        """

        #check if item in Store
        assert item_name in [item.name for item in self.store.products], 'item must be in store'
        #check if item available
        rental_item = [item for item in self.store.products
                      if item.name == item_name][0]
        
        # if item available in store, set rental time and start rental today
        if rental_item.rent(rental_time):
            self._rented_items.append(rental_item)
            self._paid[rental_item.product_id] = False
            
        # if not available, display message and all store items
        else:
            print('Sorry, {} is currently not available'.format(item_name))
            print('Here is a list of products and their availability:')
            self.store.display_products()
            
    def buy(self, item_name):
        """
        Buy item from the store if available and buyable.

        Args:
            item_name (str): Item name as given by Product.__repr__().

        Raises:
            AssertionError: If item_name not in self.store.products or item is not buyable or available.
        """
        # Check if item is in the store
        assert item_name in [item.name for item in self.store.products], 'Item must be in store'

        # Extract the item from the store
        item = next(item for item in self.store.products if item.name == item_name)

        # Check if the item is available and buyable
        if item.available and item.buyable:
            # Remove item from the store
            self.store.products.remove(item)
            # Add item to customer's owned items
            self._owned_items.append(item)
        else:
            # Print a message if the item is not available or buyable
            if not item.available:
                print(f'Sorry, {item_name} is currently not available for purchase.')
            if not item.buyable:
                print(f'Sorry, {item_name} is not buyable.')
            # Display all items with their availability
            print('Here is a list of products and their availability:')
            self.store.display_products()