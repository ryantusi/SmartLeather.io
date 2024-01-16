import pyperclip
import shutil
from pathlib import Path
from cs50 import SQL


db = SQL("sqlite:///management.db")

def copy_to_clipboard(text):
    """Copies the given text to the clipboard.

    Args:
        text (str): The text to be copied.

    Returns:
        None
    """

    pyperclip.copy(text)


def customer_exists(name):
    row = db.execute("SELECT Customer_ID FROM customers WHERE Customer_Name = ?;", name)
    if row:
        return row[0]["Customer_ID"]
    else:
        return False


def add_customer(id, name):
    db.execute("INSERT INTO customers (Customer_ID, Customer_Name) VALUES (?, ?)", id, name)


def get_customers():
    row = db.execute("SELECT * FROM customers;")
    customers = []
    for val in row:
        customers.append(val["Customer_Name"])
    return customers


def check_customer(id, name):
    row = db.execute("SELECT Customer_Name FROM customers WHERE Customer_ID = ?", id)
    if row:
        cus_name = row[0]["Customer_Name"]
        if cus_name == name:
            return True
        else:
            return False
    else:
        return False


def delete_customer(id, name):
    db.execute("DELETE FROM customers WHERE Customer_ID = ? AND Customer_Name = ?;", id, name)


def add_product(data):
    db.execute("INSERT INTO products (QR_ID, Product_ID, Product_Name, Product_Price) VALUES (?, ?, ?, ?)", data["QR_ID"], data["Product_ID"], data["Product_Name"], data["Product_Price"])


def get_products():
    row = db.execute("SELECT * FROM products;")
    products = []
    for val in row:
        products.append(val["Product_Name"])
    return products


def check_product(name, id, qr):
    row = db.execute("SELECT Product_Name FROM products WHERE Product_ID = ? AND QR_ID = ?", id, qr)
    if row:
        if row[0]["Product_Name"] == name:
            return True
        else:
            return False
    else:
        return False

def delete_product(qr_id, product_id):
    db.execute("DELETE FROM products WHERE QR_ID = ? AND Product_ID = ?", qr_id, product_id)

