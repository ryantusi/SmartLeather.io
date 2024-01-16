from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

from id_generation import qr_id_generation, job_card_generation, order_id_generation, customer_id_generation
from methods import copy_to_clipboard, customer_exists, add_customer, get_customers

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
        product_id1 = request.form.get("product_id1")

        if (product_name1 and product_id1):
            pass
        
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
                return render_template("new.html", title="creation", item="Customer", id=new_customer_id)
            else:
                id = customer_exists(new_customer)
                return render_template("error.html", code="300", message=f"Customer already exists with ID {id}")

        
        # Remove Customer
        customer_name2 = request.form.get("customer_name2")
        customer_id2 = request.form.get("customer_id2")

        if (customer_name2 and customer_id2):
            return render_template("demo.html")

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

if __name__ == '__main__':
    app.run(debug=True)
