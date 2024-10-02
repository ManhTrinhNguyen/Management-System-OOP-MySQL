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
  
class Inventory(Database):
  def __init__(self) -> None:
    super().__init__()

  def add_product(self, product):
    query='INSERT INTO products (name, description, quantity, price) VALUES (%s, %s, %s, %s)'
    self.execute(query, (product.name, product.description, product.quantity, product.price))
    print(f'Product {product.name} added to inventory')

  def update_product(self, product_id, quantity, price):
    query ="UPDATE products SET quantity = %s, price = %s WHERE product_id = %s"
    self.execute(query, (quantity, price, product_id))
    print(f"Product ID {product_id} updated.")

  def remove_product(self, product_id):
    query='DELETE FROM products WHERE product_id=%s'
    self.execute(query, (product_id,))
    print(f'Deleted product id {product_id}')

  def record_transaction(self, product_id, quantity, transaction_type):
    query='INSERT INTO transactions (product_id, quantity, transaction_type) VALUES (%s, %s, %s)'
    self.execute(query, (product_id, quantity, transaction_type))

    # Update product quantity based on transaction type
    if transaction_type == 'addition':
      self.update_product_quantity(product_id, quantity)
    elif transaction_type == 'removal':
      self.update_product_quantity(product_id, -quantity)

  def update_product_quantity(self, product_id, quantity_change):
    # Fetch current quantity 
    # Fetch the current quantity
    query = "SELECT quantity FROM products WHERE product_id = %s"
    self.cursor.execute(query, (product_id,))
    current_quantity = self.cursor.fetchone()[0]

    # Update Quantity 
    new_quantity = current_quantity + quantity_change
    self.update_product(product_id, new_quantity, None) # Update quantity without changing the Price 

  def view_product(self):
    query='SELECT * FROM products'
    self.cursor.execute(query)
    products = self.cursor.fetchall()
    for product in products:
      print(product)
      print(f"Product[ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Quantity: {product[3]}, Price: {product[4]}]")

  def generate_report(self):
    query='SELECT name, quantity FROM products'
    self.cursor.execute(query)
    report = self.cursor.fetchall()
    print("Inventory Report:")
    for name, quantity in report:
      print(f"Product: {name}, Quantity: {quantity}")

inventory = Inventory()
product_1 = Product(1, 'Iphone 14', 'Newest Iphone', 20, 5000)
product_2 = Product(3, 'Iphone 16', 'Newest Iphone', 20, 6000)

inventory.generate_report()
