from db_connector import Database 

# Product class 
class Product:
  def __init__(self, product_id, name, description, quantity, price):
    # Instances Attribute 
    self.product_id = product_id
    self.name = name 
    self.description = description 
    self.quantity = quantity
    self.price = price

  def __str__(self) -> str:
    return f"Product[ID: {self.product_id}, Name: {self.name}, Quantity: {self.quantity}, Price: {self.price}]"

# Transaction class 
class Transaction: 
  def __init__(self, transaction_id, product_id, quantity, transaction_type):
    self.transaction_id = transaction_id
    self.product_id = product_id 
    self.quantity = quantity 
    self.transaction_type = transaction_type 

  def __str__(self):
    return f"Transaction[ID: {self.transaction_id}, Product ID: {self.product_id}, Quantity: {self.quantity}, Type: {self.transaction_type}]"
  

