from product import Product
from user import User

class Cart():
  """Cart object 

  Stores items in a dictionary as product instance: quantity pair
  """

  def __init__(self, user:User) -> None:
    """Initializer for the class

    :param user: The user associated with the cart
    :type user: User
    :returns: None
    :rtype: None
    """
    self._items = {}
    self.user = user
    self._total = 0

  def __hash__(self) -> int:
    return hash((self.user,))
  
  def __eq__(self, __value: object) -> bool:
    return (isinstance(__value, type(self)) and (self.user,) == (__value.user,))

  def __str__(self) -> str:
    if self.user is None:
      return "Empty cart"
    item_str = f"{self.user}'s cart\n\n"
    count = 0
    total = 0
    item_total = 0
    item_str += "S/N\t\tItem\t\tQty\t\tPrice\t\tDiscount\tTotal\n"
    for item, qty in self._items.items():
      count += 1
      item_total = qty * item.price * (1-item.discount)
      total += item_total
      item_str += f"{count}\t\t{item.name}\t\t{qty}\t\t{item.price:0.2f}\t\t{item.discount:0.2f}\t\t{item_total:0.2f}\n"
    item_str += f"\n\t\tTotal\t\t\t\t\t\t\t\t{total:0.2f}\n"
    return item_str

  @property
  def total(self) -> float:
    self._total = 0
    for item, qty in self._items.items():
      self._total += qty * item.price * (1- item.discount)
    return float(f"{self._total:0.2f}")
  
  @property
  def items(self) -> dict:
    return self._items
  
  def add_item(self, product:Product, qty:int=1):
    """ 
    Raises TypeError if product instance is not passed\n
    Raises KeyError if product is already in cart. Try increasing item quantity in such case\n
    Raises ValueError if qty is zero or negative
    """
    if not isinstance(product, Product):
      raise TypeError("Product instance expected")
    
    if product in self._items:
      raise KeyError("Product already in cart. Increase quantity instead.")
    
    if qty <= 0:
      raise ValueError("Invalid quantity supplied")
    
    if qty > product.quantity:
      raise ValueError("Insufficient quantity")
    
    self._items[product] = qty

  def add_items(self, items):
    """ Items should be an iterable """
    if len(items) > 0:
      for item in items:
        self.add_item(item)

  def remove_item(self, product:Product):
    """ Returns None if specified product is not in cart"""
    value = self._items.pop(product, None)
    return product if value is not None else None

  def change_quantity(self, product:Product, qty:int):
    """ Removes item if quantity is less than or equal to zero"""
    if not isinstance(product, Product):
      raise TypeError("Product instance expected")
    
    if not product in self._items:
      raise KeyError("Product not found in cart")
    
    if qty <= 0:
      self._items.pop(product)
      return
     
    if qty > product.quantity:
      raise ValueError("Insufficient quantity")
    
    self._items[product] = qty

  @property
  def checkout(self):
    """ Checks if product quantities are still sufficient for checking out"""

    has_error = False
    errors = "The quantities of some items are insufficient. Try removing them or adjusting their quantity\n"
    items_to_be_checked_out = {}

    for item, qty in self._items.items():
      if item.quantity < qty:
        has_error = True
        errors += (f"Insufficent quantity available for {item.name}. Qty. Available: {item.quantity}, Qty. requested: {qty}\n")
        continue
      items_to_be_checked_out[item] = qty
    
    if has_error:
      raise ValueError(errors)
    
    for item, qty in items_to_be_checked_out.items():
      item.quantity -= qty

    receipt = print(self)
    self.clear()
    return receipt

  def clear(self):
    self.user = None
    self._items.clear()

if __name__ == "__main__":
  prod1 = Product("Mango", 99.99, 10)
  prod2 = Product("Pear", 350, 50)
  prod3 = Product("Apple", 300.50, 30)

  user1 = User("Maurice", 123)

  cart1 = Cart(user1)
  cart1.add_item(prod1)
  cart1.add_item(prod3, 5)
  cart1.change_quantity(prod1, 7)
  cart1.add_item(prod2, 2)
  cart1.remove_item(prod1)
  print(cart1)
  cart1.checkout
  print(cart1)

  