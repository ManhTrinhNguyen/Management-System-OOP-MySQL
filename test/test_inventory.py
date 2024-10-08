from unittest.mock import MagicMock, patch
import unittest
import pytest 
import sys 

sys.path.insert(1, '/Users/trinhnguyen/Documents/Meta-Certificate/Database/Management-System-OOP-MySQL/')
from main import Inventory, Product, Transaction
from db_connector import Database

class TestInventory(unittest.TestCase):

  @patch('mysql.connector.connect')
  def setUp(self, mock_connect): # mock_connect is arg as the mysq.connector.connect
    # Mocking DB and Cursor 
    self.mock_db = MagicMock()
    self.mock_cursor = MagicMock()

    # mock_connect will return value as the mock_db
    mock_connect.return_value = self.mock_db

    # self.mock_db will return value as self.mock cursor 
    self.mock_db.cursor.return_value = self.mock_cursor

    # Initialize the Inventory class with the mock database
    self.db = Database()
    self.inventory = Inventory(self.db)

    # Create a product instance to use in tests
    self.product = Product(1, 'Iphone 14', 'Newest Iphone', 20, 5000)


  def test_add_product(self):
    """Test case for adding a product."""
    # Call the method want to test (add_product)
    self.inventory.add_product(self.product)
    
    # Assert that the SQL query was executed correctly
    self.mock_cursor.execute.assert_called_with(
      'INSERT INTO products (name, description, quantity, price) VALUES (%s, %s, %s, %s)',
      (self.product.name, self.product.description, self.product.quantity, self.product.price)
    )

    # Assert that the commit was called once
    self.mock_db.commit.assert_called_once()

  def test_update_product(self):
    # Call method want to test
    self.inventory.update_product(self.product.product_id, self.product.quantity, self.product.price)

    # Assert that the SQL query was executed correctly 
    self.mock_cursor.execute.assert_called_with(
      'UPDATE products SET quantity = %s, price = %s WHERE product_id = %s',
      (self.product.quantity, self.product.price, self.product.product_id)
    )
    # Assert that the commit was called once
    self.mock_db.commit.assert_called_once()

  def test_remove_product(self):
    # Call method want to test
    self.inventory.remove_product(self.product.product_id)

    # Assert that the SQL query was executed correctly 
    self.mock_cursor.execute.assert_called_with(
      'DELETE FROM products WHERE product_id=%s',
      (self.product.product_id,)
    )
    # Assert that the commit was called once 
    self.mock_db.commit.assert_called_once()

  def test_record_transaction(self):
    # CAll method want to test
    self.inventory.record_transaction(self.product.product_id, self.product.quantity, 'addition')

    # Assert that the INSERT query was executed correctly
    insert_call = unittest.mock.call(
      'INSERT INTO transactions (product_id, quantity, transaction_type) VALUES (%s, %s, %s)',
      (self.product.product_id, self.product.quantity, 'addition')
    )

    # Assert that the UPDATE query was executed correctly 
    update_call = unittest.mock.call(
      "UPDATE products SET quantity = %s, price = %s WHERE product_id = %s",
      (self.mock_cursor.fetchone().__getitem__().__add__(), None, self.product.product_id)
    )

    # Assert both calls (INSERT and UPDATE) were made 
    self.mock_cursor.execute.assert_has_calls([insert_call, update_call], any_order=True)
    # Assert that commit was called
    self.mock_db.commit.assert_called()
    
  def test_update_product_quantity(self):
    # Call Method want to test
    self.inventory.update_product_quantity(self.product.product_id, 10)

    # Assert that the Select query was executed correctly 
    select_call = unittest.mock.call(
      'SELECT quantity FROM products WHERE product_id = %s',
      (self.product.product_id,)
    )
    # Assert that the UPDATE query was executed correctly 
    update_call = unittest.mock.call(
      'UPDATE products SET quantity = %s, price = %s WHERE product_id = %s',
      (self.mock_cursor.fetchone().__getitem__().__add__(), None, self.product.product_id)
      )

    # Assert both calls (Insert and update) were made 
    self.mock_cursor.execute.assert_has_calls([select_call, update_call], any_order=True)

    self.mock_db.commit.assert_called()

  def test_view_product(self):
    # Call method want to test
    self.inventory.view_product()

    # Assert that the Select was execute correctly
    self.mock_cursor.execute.assert_called_with(
      'SELECT * FROM products'
    )
    # No need to check for commit in a SELECT query.
  