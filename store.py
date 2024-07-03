from products import Product, Laptop, Phone

NoneType = type(None) 

class RentalStore():
    """
    Container to store products.
    
    Args:
        products (list): List of products in store. Defaults to empty list.

    """
    def __init__(self, products=None):
        if isinstance(products, NoneType):
            products = []
        assert type(products) == list, "The input argument needs to be a list."
        for item in products:
            assert isinstance(item, Product), "only Product-type are allowed to be in rental store"
        self.products = products
    
    @staticmethod
    def display_impressum():
        print('IMPRINT \nRentalStore GmbH \nDeposit Street 7 \n44321 Rent City')
       
    def display_products(self):
        """Displays Products with name, price per week and availability."""
        for item in self.products: 
            print(
                "Name: {}, Price per week: {:.2f}€, Available: {}, Buyable: {}".format(
                item.name,
                item.price_per_week,
                item.available,
                item.buyable
                )
            )
            
    def __len__(self):
        """Return the number of products in the store."""
        return len(self.products)
    
    def __add__(self, item):
        """Add a product to the store."""
        assert isinstance(item, Product), "Only instances of Product can be added to the store"
        
        self.products.append(item)
        print('{} is added to the store'.format(item.__repr__()))
        return self
            
    def __sub__(self, item):
        """Remove a product from the store."""
        assert isinstance(item, Product), "Only instances of Product can be removed from the store"
        
        for product in self.products:
            if product.name == item.name:
                self.products.remove(product)
                return self
            
        print('{} cannot be removed, as it is not part of the store\'s products'.format(item.__repr__()))
        return self