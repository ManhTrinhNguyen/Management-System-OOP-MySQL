from dotenv import load_dotenv
import mysql.connector
import os 

# Load environment variables from .env file
load_dotenv()

# Database connect class 
class Database: 
  def __init__(self) -> None:
    self.db = mysql.connector.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host='localhost', database='inventory_db')
    self.cursor = self.db.cursor()

  def execute(self, query, data=None):
    self.cursor.execute(query, data)
    self.db.commit()

  def fetch_all_data(self, query, data=None):
    self.cursor.execute(query, data)
    return self.cursor.fetchall()
  
  def close(self):
    self.cursor.close()
    self.db.close()

db = Database()