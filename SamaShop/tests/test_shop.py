from unittest import TestCase
from shop import Shop
from product import Product
from cart import Cart
from user import User

class ShopTest(TestCase):
  def setUp(self) -> None:
    self.shop = Shop("Sama Shop")
    self.prod1 = self.shop.add_product("Banana", 200, 10)
    self.user = self.shop.add_user("user@example.com", 123)
    self.cart = self.shop.create_cart(self.user)

  def test_add_product_raises_key_error_if_product_already_in_shop(self):
    with self.assertRaises(KeyError):
      self.shop.add_product("Banana", 100, 10)

  def test_add_product_returns_product_on_success(self):
    product = self.shop.add_product("Pear", 150, 10)
    self.assertIsInstance(product, Product)
    self.assertEqual(product.name, "Pear")

  def test_get_product_returns_none_if_product_not_found(self):
    product = self.shop.get_product("Pear")
    self.assertIsNone(product)

  def test_get_product_returns_product_if_found(self):
    product = self.shop.get_product("Banana")
    self.assertEqual(product.name, "Banana")

  def test_add_user_raises_valueerror_on_duplicate_email(self):
    with self.assertRaises(ValueError):
      self.shop.add_user("user@example.com", 456)

  def test_add_user_returns_user_on_success(self):
    user = self.shop.add_user("test@example.com", 123)
    self.assertIsInstance(user, User)
    self.assertEqual(user.email, "test@example.com")

  def test_create_cart_does_not_allow_duplicate_users(self):
    self.shop.create_cart(self.user)
    self.assertEqual(len(self.shop.carts), 1)

  def test_create_cart_returns_old_cart_on_duplicate_users(self):
    self.cart.add_item(self.prod1)
    gotten_cart = self.shop.create_cart(self.user)
    self.assertEqual(self.cart, gotten_cart)

  def test_create_cart_returns_cart_on_success(self):
    user = self.shop.add_user("test@example.com", 123)
    cart = self.shop.create_cart(user)
    self.assertIsInstance(cart, Cart)
    self.assertEqual(cart.user, user)

  def test_get_cart_returns_none_if_cart_associated_with_user_is_not_found(self):
    user = self.shop.add_user("test@example.com", 123)
    cart = self.shop.get_cart(user)
    self.assertIsNone(cart)

  def test_get_cart_returns_cart_on_success(self):
    cart = self.shop.get_cart(self.user)
    self.assertIsInstance(cart, Cart)
    self.assertEqual(cart.user, self.user)

  def test_get_user_returns_none_if_user_not_found(self):
    user = self.shop.get_user("test@example.com")
    self.assertIsNone(user)

  def test_get_user_returns_user_on_success(self):
    user = self.shop.get_user("user@example.com")
    self.assertIsInstance(user, User)
    self.assertEqual(user, self.user)

  def test_checkout_raises_attributeerror_when_cart_not_associated_with_user(self):
    self.cart.user = None
    with self.assertRaises(AttributeError):
      self.shop.checkout(self.cart)

  def test_checkout_raises_exception_when_items_not_in_cart(self):
    self.cart.items.clear()
    with self.assertRaises(Exception):
      self.shop.checkout(self.cart)

