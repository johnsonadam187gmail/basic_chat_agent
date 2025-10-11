from pydantic import BaseModel
from openai import OpenAI
import time
from packages.environment import load_keys, pdf_reader, read_text_file_to_string
import sqlite_utils

db = sqlite_utils.Database("test_db.db")

# Sample data for a 'products' table
products = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 1200.00},
    {"id": 2, "name": "Coffee Maker", "category": "Home Goods", "price": 85.50},
    {"id": 3, "name": "Keyboard", "category": "Electronics", "price": 75.00},
    {"id": 4, "name": "Desk Lamp", "category": "Home Goods", "price": 35.99},
    {"id": 5, "name": "Mouse", "category": "Electronics", "price": 25.00},
]

# Insert the data into a table named 'products'
# The 'pk="id"' ensures the 'id' field is the primary key.
db["products"].insert_all(products, pk="id", replace=True)

print("Database 'test_db.db' created and populated with 5 products.")



