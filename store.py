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