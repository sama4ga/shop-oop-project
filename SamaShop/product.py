
class Product():
  """ Product class """
  
  def __init__(self, name:str, price:int|float, quantity:int, discount:float=0) -> None:
    self.name = name
    self.price = price
    self.quantity = quantity
    self.discount = discount

  def __str__(self) -> str:
    return f"Name:{self.name}\t\tPrice:{self.price}\t\tQuantity:{self.quantity}\t\tDiscount:{self.discount}"

  def __hash__(self) -> int:
    return hash((self.name,))
  
  def __eq__(self, __value: object) -> bool:
    return (isinstance(__value, type(self)) and (self.name,) == (__value.name,))
