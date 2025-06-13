from unittest import TestCase
from user import User
from cart import Cart
from product import Product

class CartTest(TestCase):
  def setUp(self) -> None:
    user = User("test1@example.com", 1234)
    self.cart = Cart(user)
    self.prod1 = Product("Mango", 50.00, 5)
    self.prod2 = Product("Apple", 100.00, 5)
    self.prod3 = Product("Pear", 200.00, 5)

  def test_add_item_raises_typeerror_if_product_instance_not_passed(self):
    with self.assertRaises(TypeError):
      self.cart.add_item("Mango")

  def test_add_item_raises_keyerror_if_product_already_exists(self):
    self.cart.add_item(self.prod1)
    with self.assertRaises(KeyError):
      self.cart.add_item(self.prod1)

  def test_add_item_raises_valueerror_if_quantity_is_le_zero(self):
    with self.assertRaises(ValueError):
      self.cart.add_item(self.prod1, 0)

  def test_add_item_raises_valueerror_if_quantity_is_gt_product_quantity(self):
    with self.assertRaises(ValueError):
      self.cart.add_item(self.prod1, 7)

  def test_add_item_successfully_adds_items_to_cart(self):
    self.cart.add_item(self.prod1)
    self.assertDictEqual(self.cart.items, {self.prod1:1})

  def test_remove_item_returns_none_if_item_not_found(self):
    self.cart.add_item(self.prod1)
    item = self.cart.remove_item(self.prod2)
    self.assertIsNone(item)

  def test_remove_item_returns_removed_item_and_removes_it_from_cart(self):
    self.cart.add_item(self.prod1)
    self.cart.add_item(self.prod2)
    prod1 = self.cart.remove_item(self.prod1)
    self.assertEqual(prod1, self.prod1)
    self.assertDictEqual(self.cart.items, {self.prod2:1})    

  def test_change_quantity_raises_typeerror_if_product_instance_not_passed(self):
    self.cart.add_item(self.prod1)
    with self.assertRaises(TypeError):
      self.cart.change_quantity("Mango", 4)

  def test_change_quantity_raises_keyerror_if_product_is_not_in_cart(self):
    self.cart.add_item(self.prod1)
    with self.assertRaises(KeyError):
      self.cart.change_quantity(self.prod2, 4)

  def test_change_quantity_removes_item_if_quantity_is_le_zero(self):
    self.cart.add_item(self.prod1)
    self.cart.change_quantity(self.prod1, 0)
    self.assertCountEqual(self.cart.items, {})

  def test_change_quantity_raises_valueerror_if_quantity_is_gt_product_quantity(self):
    self.cart.add_item(self.prod1)
    with self.assertRaises(ValueError):
      self.cart.change_quantity(self.prod1, 7)

  def test_change_quantity_successfully_changes_quantity(self):
    self.cart.add_item(self.prod1)
    self.cart.change_quantity(self.prod1, 3)
    self.assertDictEqual(self.cart.items, {self.prod1:3})

  def test_cart_total_amount(self):
    self.cart.add_item(self.prod1)
    self.cart.add_item(self.prod2, 5)
    total = self.cart.total
    self.assertEqual(total, 550.00)

  def test_cart_items(self):
    self.cart.add_item(self.prod1)
    self.cart.add_item(self.prod2)
    items = self.cart.items
    self.assertEqual(len(items), 2)

  def test_checkout(self):
    self.cart.add_item(self.prod1)
    self.cart.add_item(self.prod2)
    receipt = self.cart.checkout
    self.assertEqual(self.cart.user, None) and self.assertEqual(len(self.cart.items), 0)  

  def test_checkout_raises_when_quantity_is_less(self):
    self.cart.add_item(self.prod1, 4)
    self.prod1.quantity = 3
    with self.assertRaises(ValueError):
      self.cart.checkout