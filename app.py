from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, send_file
from flask_session import Session

from qr_scan import QRScanner
from qr_generator import generate_qr_code
from id_generation import product_id_generation, job_card_generation, order_id_generation, customer_id_generation, qr_id_generation
from methods import copy_to_clipboard, customer_exists, add_customer, get_customers, check_customer, delete_customer, get_products, add_product, check_product, delete_product, add_order, check_order, delete_order

app = Flask(__name__)
db = SQL("sqlite:///management.db")
qr_scanner = QRScanner()

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/demo", methods=["GET", "POST"])
def demo():
    if request.method == "GET":
        CUSTOMERS = get_customers()
        PRODUCTS = get_products()
        return render_template("demo.html", customers = CUSTOMERS, products = PRODUCTS)
    else:
        # New Product
        product_name1 = request.form.get("product_name1")
        product_price = request.form.get("product_price")

        if (product_name1 and product_price):
            product_id = product_id_generation("PVTLTD786")
            qr_id = qr_id_generation("PVTLTD786")
            qr_details = {
                "QR_ID": qr_id,
                "Product_ID": product_id,
                "Product_Name": product_name1,
                "Product_Price": product_price
            }
            generate_qr_code(qr_details)
            add_product(qr_details)
            return render_template("product.html", title="creation", item="Product", content=f"QR-ID: {qr_id} Product-ID: {product_id}", id=qr_id)
        
        # Delete Product
        product_name2 = request.form.get("product_name2")
        product_id2 = request.form.get("product_id2")
        qr_id2 = request.form.get("qr_id")

        if (qr_id2 and product_id2):
            if check_product(product_name2, product_id2, qr_id2):
                return render_template("delete_product.html", item="Product", name=product_name2, id1=qr_id2, id2=product_id2)
            else:
                return render_template("error.html", code=300, message="Product ID or QR ID not correct for the product")

        # New Order
        customer_id = request.form.get("customer_id")
        product_id3 = request.form.get("product_id3")
        quantity = request.form.get("quantity")

        if (customer_id and product_id3):
            check_p = db.execute("SELECT * FROM products WHERE Product_ID = ?", product_id3)
            check_c = db.execute("SELECT * FROM customers WHERE Customer_ID = ?", customer_id)
            if not (check_p and check_c):
                return render_template("error.html", code=300, message="Incorrect Information Submitted")
            else:
                new_order_id = order_id_generation("PVTLTD786")
                add_order(new_order_id, customer_id, product_id3, quantity)
                return render_template("order.html", item="Order", content=f"Order ID: {new_order_id}")

        # New Customer
        new_customer = request.form.get("new_customer_name")

        if (new_customer):
            if customer_exists(new_customer) == False:
                new_customer_id = customer_id_generation("PVTLTD786")
                add_customer(new_customer_id, new_customer)
                return render_template("customer.html", title="creation", item="Customer", content=new_customer_id)
            else:
                id = customer_exists(new_customer)
                return render_template("error.html", code="300", message=f"Customer already exists with ID {id}")

        
        # Remove Customer
        customer_name2 = request.form.get("customer_name2")
        customer_id2 = request.form.get("customer_id2")

        if (customer_name2 and customer_id2):
            if check_customer(customer_id2, customer_name2):
                return render_template("delete_customer.html", item="Customer", id=customer_id2, name=customer_name2)
            else:
                return render_template("error.html", code=300, message="Customer ID not matched")

        # Cancel Order
        customer_id3 = request.form.get("customer_id3")
        order_id = request.form.get("order_id")
        DATE = request.form.get("date")

        if (order_id and DATE):
            if check_order(order_id, customer_id3):
                return render_template("delete_order.html", item="Order", id1=order_id, id2=customer_id3, date=DATE)
            else:
                return render_template("error.html", code=300, message="Order ID incorrect")

        return render_template("demo.html")

@app.route("/customer", methods=["POST"])
def customer():
    if request.method == "POST":
        value = request.form.get("hidden")
        copy_to_clipboard(value)
        return redirect("/demo")

@app.route("/product", methods=["GET", "POST"])
def product():
    if request.method == "POST":
        file = request.form.get("hidden1")
        filename = f"static/QR_codes/{file}.png"
        return send_file(filename, as_attachment=True)
    elif request.method == "GET":
        value = request.args.get("hidden2")
        copy_to_clipboard(value)
        return redirect("/demo")

@app.route("/deletecustomer", methods=["POST"])
def deletecustomer():
    if request.method == "POST":
        id = request.form.get("hidden_id")
        name = request.form.get("hidden_name")
        delete_customer(id, name)
        return redirect("/demo")

@app.route("/deleteproduct", methods=["POST"])
def deleteproduct():
    if request.method == "POST":
        qr = request.form.get("hidden_id1")
        id = request.form.get("hidden_id2")
        delete_product(qr, id)
        return redirect("/demo")

@app.route("/order", methods=["POST"])
def order():
    if request.method == "POST":
        value = request.form.get("hidden")
        copy_to_clipboard(value)
        return redirect("/demo")

@app.route("/deleteorder", methods=["POST"])
def deleteorder():
    if request.method == "POST":
        id1 = request.form.get("hidden1")
        id2 = request.form.get("hidden2")
        date = request.form.get("hidden3")
        delete_order(id1, id2, date)
        return redirect("/demo")
    
@app.route("/scan", methods=["GET", "POST"])
def scanpage():
    if request.method == "GET":
        return render_template("scan.html")

@app.route('/start_scanner')
def start_scanner():
    qr_scanner.start_scanner()
    data = qr_scanner.get_scanned_data()
    return 'Scanner started'

@app.route('/stop_scanner')
def stop_scanner():
    qr_scanner.stop_scanner()
    return 'Scanner stopped'

if __name__ == '__main__':
    app.run(debug=True)
