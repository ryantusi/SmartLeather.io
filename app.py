from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)

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
        return render_template("demo.html")
    else:
        product_name1 = request.form.get("product_name1")
        product_id1 = request.form.get("product_id1")

        if not (product_name1 and product_id1):
            pass

        product_name2 = request.form.get("product_name2")
        product_id2 = request.form.get("product_id2")
        qr_id = request.form.get("qr_id")

        if not (product_name2 and product_id2):
            pass

        customer_name = request.form.get("customer_name")
        customer_id = request.form.get("customer_id")
        product_id3 = request.form.get("product_id3")
        quantity = request.form.get("quantity")

        if not (customer_id and customer_name):
            pass

        return render_template("demo.html")

if __name__ == '__main__':
    app.run(debug=True)
