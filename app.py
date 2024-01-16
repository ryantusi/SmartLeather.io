from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

from qr_generator import generate_qr_code
from id_generation import product_id_generation, job_card_generation, order_id_generation, customer_id_generation, qr_id_generation
from methods import copy_to_clipboard, customer_exists, add_customer, get_customers, check_customer, delete_customer, add_product

app = Flask(__name__)
db = SQL("sqlite:///management.db")

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
        return render_template("demo.html", customers = CUSTOMERS)
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
            return render_template("new.html", title="creation", item="Product", content=f"QR-ID: {qr_id} Product-ID: {product_id}", id=qr_id)
        
        # Delete Product
        product_name2 = request.form.get("product_name2")
        product_id2 = request.form.get("product_id2")
        qr_id = request.form.get("qr_id")

        if (product_name2 and product_id2):
            pass

        # New Order
        customer_name = request.form.get("customer_name")
        customer_id = request.form.get("customer_id")
        product_id3 = request.form.get("product_id3")
        quantity = request.form.get("quantity")

        if (customer_id and customer_name):
            pass

        # New Customer
        new_customer = request.form.get("new_customer_name")

        if (new_customer):
            if customer_exists(new_customer) == False:
                new_customer_id = customer_id_generation("PVTLTD786")
                add_customer(new_customer_id, new_customer)
                return render_template("new.html", title="creation", item="Customer", content=new_customer_id)
            else:
                id = customer_exists(new_customer)
                return render_template("error.html", code="300", message=f"Customer already exists with ID {id}")

        
        # Remove Customer
        customer_name2 = request.form.get("customer_name2")
        customer_id2 = request.form.get("customer_id2")

        if (customer_name2 and customer_id2):
            if check_customer(customer_id2, customer_name2):
                return render_template("delete.html", item="Customer", id=customer_id2, name=customer_name2)
            else:
                return render_template("error.html", code=300, message="Customer ID not matched")

        # Cancel Order
        order_id = request.form.get("order_id")
        job_card = request.form.get("job_card")

        if (order_id and job_card):
            pass

        return render_template("demo.html")

@app.route("/new", methods=["POST"])
def new():
    if request.method == "POST":
        value = request.form.get("hidden")
        copy_to_clipboard(value)
        return redirect("/demo")

@app.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        id = request.form.get("hidden_id")
        name = request.form.get("hidden_name")
        delete_customer(id, name)
        return redirect("/demo")

if __name__ == '__main__':
    app.run(debug=True)
