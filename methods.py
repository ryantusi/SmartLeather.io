import pyperclip
from cs50 import SQL


db = SQL("sqlite:///management.db")

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

def copy_to_clipboard(text):
    """Copies the given text to the clipboard.

    Args:
        text (str): The text to be copied.

    Returns:
        None
    """

    pyperclip.copy(text)

