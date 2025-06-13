from cart import Cart
from user import User
from product import Product

class Shop():
  """ Shop object"""

  def __init__(self, name:str) -> None:
    self.name = name
    self._carts = set()
    self._users = set()
    self._products = set()

  def __str__(self) -> str:
    shop_str = f"{self.name}\n\nProducts\n"
    shop_str += f"Name\t\tPrice\t\tQuantity\tDiscount\n"
    for product in self._products:
      shop_str += f"{product.name}\t\t{product.price}\t\t{product.quantity}\t\t{product.discount}\n"

    shop_str += "\nUsers\n"
    for user in self._users:
      shop_str += f"{user}\n"

    shop_str += "\nCarts\n"
    for cart in self._carts:
      shop_str += f"{cart}\n"

    return shop_str

  @property
  def users(self):
    return self._users

  @property
  def carts(self):
    return self._carts

  @property
  def products(self):
    return self._products

  def add_product(self, name:str, price:int|float, quantity:int, discount:float=0):
    product = Product(name=name, price=price, quantity=quantity, discount=discount)
    if product in self._products:
      raise KeyError("Product already in shop")
    self._products.add(product)
    return product
  
  def get_product(self, name:str) -> Product|None:
    for product in self._products:
      if product.name == name:
        return product
    return None

  def add_user(self, email:str, password:str):
    if not self._validate_user_details(email):
      raise ValueError("Duplicate email supplied")
    user = User(email=email, password=password)
    self._users.add(user)
    return user

  def _validate_user_details(self, email:str):
    for user in self._users:
      if user.email == email:
        return False
    return True

  def create_cart(self, user:User) -> Cart:
    cart = self.get_cart(user)
    if cart is None:
      cart = Cart(user)
      self._carts.add(cart)
    return cart
  
  def get_cart(self, user:User) -> Cart|None:
    """ Returns None if cart is not found"""
    for cart in self._carts:
      if cart.user == user:
        return cart
    return None

  def get_user(self, email:str) -> User|None:
    """ Returns None if user is not found"""
    for user in self._users:
      if user.email == email:
        return user
    return None

  def user_login(self, email:str, password:str) -> User|None:
    """ Returns None if user is not found"""
    for user in self._users:
      if user.email == email and user.password == password:
        return user
    return None

  def checkout(self, cart:Cart):
    if cart.user is None:
      raise AttributeError("Cart not attributed to a user")
    
    if len(cart.items) < 1:
      raise Exception("No items in cart")
    
    cart.checkout
    self._carts.remove(cart)

  

if __name__ == "__main__":
  # create shop
  samaShop = Shop("Sama Shop")

  # create users
  samaShop.add_user("test1@example.com", "123") 
  samaShop.add_user("test2@example.com", "123") 
  samaShop.add_user("test3@example.com", "123") 

  # create products
  samaShop.add_product("Pear", 249.99, 200) 
  samaShop.add_product("Mango", 99.99, 50) 
  samaShop.add_product("Apple", 249.50, 150) 
  samaShop.add_product("Cherry", 49.99, 200) 
  samaShop.add_product("Pawpaw", 149.99, 100)

  test1 = samaShop.get_user("test1@example.com")
  cart1 = samaShop.create_cart(test1)

  pear = samaShop.get_product("Pear")
  apple = samaShop.get_product("Apple")
  mango = samaShop.get_product("Mango")
  cart1.add_item(pear)
  cart1.add_item(apple)
  cart1.add_item(mango, 5)

  try:
    receipt = cart1.checkout
    print(receipt)
  except ValueError as ex:
    print(ex)


  print(samaShop)
  
