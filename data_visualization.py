from cs50 import SQL
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

db = SQL("sqlite:///management.db")

def revenue_chart():
    rows = db.execute("SELECT MONTH FROM revenue WHERE YEAR = 2023")
    months = [row["MONTH"] for row in rows]

    rows = db.execute("SELECT Total_Revenue FROM revenue WHERE YEAR = 2023")
    revenue = [row["Total_Revenue"] for row in rows]
    
    plt.plot(months, revenue, color="#FF5733", label="Revenue (per month) for 2023", linestyle='-', marker='o', markersize=8)
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.title("Revenue (per month) for 2023")

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.gca().set_facecolor('#E6E6FA')

    plt.tight_layout()
    plt.savefig("static/graphs/revenue.png")

def top_customers():
    rows = db.execute("SELECT Customer_ID, COUNT(*) AS Frequency FROM orders GROUP BY Customer_ID ORDER BY Frequency DESC LIMIT 3;")
    top_customers = [row["Customer_ID"] for row in rows]
    counts = [row["Frequency"] for row in rows]
    names = []
    for id in top_customers:
        row = db.execute("SELECT Customer_Name FROM customers WHERE Customer_ID = ?", id)
        names.append(row[0]["Customer_Name"])
    colors = ["#B85042", "#A7BEAE", "#E7E8D1"]
    explode = (0.1, 0, 0)
    plt.pie(counts, labels=names, startangle=90, colors=colors, explode=explode, shadow=True)
    plt.title('Our Top Three Most Frequent Customers')
    plt.tight_layout()
    plt.savefig("static/graphs/customers.png")

def top_products():
    rows = db.execute("SELECT Product_ID, COUNT(*) AS Frequency FROM orders GROUP BY Product_ID ORDER BY Frequency DESC LIMIT 3;")
    top_products = [row["Product_ID"] for row in rows]
    counts = [row["Frequency"] for row in rows]
    names = []
    for id in top_products:
        row = db.execute("SELECT Product_Name FROM products WHERE Product_ID = ?", id)
        names.append(row[0]["Product_Name"])
    colors = ["#DDC3A5", "#201E20", "#E0A96D"]
    explode = (0.1, 0, 0)
    plt.pie(counts, labels=names, startangle=90, colors=colors, explode=explode, shadow=True)
    plt.title('Our Top Three Hot Selling Products')
    plt.tight_layout()
    plt.savefig("static/graphs/products.png")

def gauge(meter, id):
    # Sample data
    completed = meter
    total = 100

    # Create a gauge chart with improved styling
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=completed,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, total], 'tickmode': 'linear', 'tick0': 0, 'dtick': 20},
            'bar': {'color': "#B85042"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, total], 'color': "#A7BEAE"},
            ]
        },
        number={'valueformat': 'd', 'font': {'size': 40}},
        title={'text': "Completion", 'font': {'size': 20}}
    ))

    # Update layout for better appearance
    fig.update_layout(
        title_text=f'Job Card: {id} Gauge Chart',
        height=400,
        paper_bgcolor="#E7E8D1"
    )

    # Save the chart as an image
    chart_html = pio.to_html(fig, full_html=False)

    return chart_html

def job_charts():
    rows = db.execute("SELECT Job_Card, Completed, Total FROM jobs")
    job_cards = [row["Job_Card"] for row in rows]
    completes = [row["Completed"] for row in rows]
    totals = [row["Total"] for row in rows]
    length = len(rows)
    charts = []
    for i in range(length):
        complete = int(completes[i])
        total = int(totals[i])
        job = job_cards[i]
        perc = round((complete / total) * 100)
        charts.append(gauge(perc, job))
    return charts

