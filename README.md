# Proxima SmartManage: SmartLeather.io 🚀

Welcome to **SmartLeather.io**, the groundbreaking product brought to you by Proxima SmartManage. 🌐

SmartLeather.io is a specialized software solution meticulously crafted for the dynamic leather industry. Embracing cutting-edge AI technology, this platform redefines manufacturing operations and propels business growth into a new era. 🛠️

## Repository Structure 📂

### Static
- `Assets`: Contains all images for the web app.
- `Graphs`: Houses data visualization images for the web app.
- `QR_Codes`: Stores all QR codes generated from the web app.
- `screenshots`: snapshots of the working web app

### Templates
- `HTML Files`: A collection of essential HTML files for various functionalities.
   - `index.html`  `demo.html`  `customer.html`  `delete_customer.html`  `product.html`  `delete_product.html`  `order.html`  `delete_order.html`  `scan.html`  `error.html`

### Modules
- `app.py`: Main Flask app importing other customized Python modules with a connected database for efficient management.
- `data_visualization.py`: Methods for creating graphs and charts for the live dashboard.
- `download_excel.py`: A method facilitating the download of the 'management.xlsx' file.
- `id_generation.py`: Methods to generate unique IDs for products, customers, orders, and jobs.
- `methods.py`: Centralized operations for checking, creating, and deleting products, customers, and orders data in the database.
- `qr_generator.py`: Generates QR codes for newly created orders and saves them.
- `qr_scan.py`: A method opening the QR scanner to scan QR codes and update the database.

### Database & Files
- `management.db`: The database containing tables for constant operations, customers, jobs, orders, products, and revenue.
- `management.xlsx`: An Excel sheet downloading all database tables as separate sheets into a single document.

### Miscellaneous
- `requirements.txt`: Lists all the requirements for the app to function.

## How to Use the App 🚀

### Step 1: Explore the Live Dashboard
Access the software platform using your credentials and navigate to the live dashboard for real-time analytics. Leverage interactive tools to analyze key metrics and download raw data for in-depth examination of operational insights.

### Step 2: Complete Forms for Seamless Management
Locate and fill in the necessary product, customer, or order management forms, ensuring accuracy and completeness. Each entry receives a unique identification number, and for orders, a QR code is generated for easy tracking throughout the manufacturing process.

### Step 3: Initiate Scanning Demo for Hands-On Experience
Create a new order through the interface to initiate the scanning demo. Observe live dashboard updates reflecting changes in key metrics and data points, providing a firsthand look at the software's responsiveness and real-time monitoring capabilities.

## Snapshots 📸

![screenshots](/static/snapshots/SLIO1.gif)
![screenshots](/static/snapshots/SLIO2.gif)
![screenshots](/static/snapshots/SLIO3.png)

Feel free to explore, innovate, and witness the transformative power of SmartLeather.io! 🔍💡

## How to Run the App 🏃‍♂️

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
2. **Run the Flask App**
   ```bash
   flask run

## Contributions 🤝

We welcome contributions to enhance and extend SmartLeather.io. If you have ideas, bug fixes, or new features to propose, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear messages.
4. Push your changes to your fork.
5. Create a pull request, explaining your changes and why they should be merged.

Thank you for contributing to SmartLeather.io! 🙌