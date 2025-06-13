#!/usr/bin/env python3

class User():
  def __init__(self, email:str, password:str) -> None:
    self.email = email
    self.password = password

  def __str__(self) -> str:
    return self.email