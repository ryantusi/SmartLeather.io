from cs50 import SQL
from datetime import datetime
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time
import json

db = SQL("sqlite:///management.db")

class QRScanner:
    def __init__(self):
        self.cap = None
        self.scanned_data = []

    def segregate_timestamp(self, timestamp_str):
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second

    def start_scanner(self, camera_index=0, delay_between_scans=3):
        self.cap = cv2.VideoCapture(camera_index)
        last_process_time = 0

        while True:
            _, frame = self.cap.read()

            # Convert the frame to grayscale for better QR code detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect QR codes in the frame
            decoded_objects = decode(gray)

            for obj in decoded_objects:
                # Draw a rectangle around the QR code
                points = obj.polygon
                if len(points) == 4:
                    pts = np.array([(point.x, point.y) for point in points], dtype=int)
                    cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

                    # Get the QR code data
                    details = obj.data.decode('utf-8')
                    try:
                        # Try to decode the JSON-formatted string into a Python dictionary
                        details_dict = json.loads(details)

                        # Get the current timestamp
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        details_dict["Timestamp"] = timestamp

                    except json.JSONDecodeError as e:
                        # Handle the case where the data is not valid JSON
                        print(f"Error decoding JSON: {e}")

                    # Check if the specified delay has passed since the last processed QR code
                    current_time = time.time()
                    if current_time - last_process_time >= delay_between_scans:
                        last_process_time = current_time

                        # Do something with the QR code data and timestamp (e.g., print them)
                        #print(f"Scanned QR Code: {details_dict}")

                        # Display the QR code data and timestamp on the frame
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        bottom_left_corner = (pts[0][0], pts[0][1] - 10)
                        font_scale = 0.5
                        font_color = (255, 255, 255)
                        line_type = 1
                        cv2.putText(frame, f"ID: {details_dict} | Time: {timestamp}", bottom_left_corner, font, font_scale, font_color, line_type)

                        # Append the details to the list
                        self.scanned_data.append(details_dict)
                        if self.check_data(details_dict):
                            self.update_data(details_dict)
                            self.stop_scanner()
                        else:
                            self.write_data(details_dict)

                        # Segregate the timestamp components
                        #year, month, day, hour, minute, second = self.segregate_timestamp(timestamp)
                        #print(f"Year: {year}, Month: {month}, Day: {day}, Hour: {hour}, Minute: {minute}, Second: {second}")

            # Display the frame with the rectangles around the QR codes
            cv2.imshow("QR Code Scanner", frame)

            # Non-blocking wait key
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # Press 'Esc' to exit
                break


    def stop_scanner(self):
        if self.cap is not None:
            self.cap.release()
            cv2.destroyAllWindows()

    def get_scanned_data(self):
        return self.scanned_data

    def clear_scanned_data(self):
        self.scanned_data = []

    def add_revenue(self, data):
        product_id = data["Product_ID"]
        quantity = int(data["Quantity"])
        price = db.execute("SELECT Product_Price FROM products WHERE Product_ID = ?", product_id)
        product_price = price[0]["Product_Price"]
        total_price = float(product_price) * quantity 
        year, month, day, hour, minute, second = self.segregate_timestamp(data["Timestamp"])
        row = db.execute("SELECT * FROM revenue WHERE YEAR = ? AND MONTH = ?", year, month)

        if row:
            db.execute("UPDATE revenue SET Total_Revenue = Total_Revenue + ? WHERE YEAR = ? AND MONTH = ?", total_price, year, month)
        else:
            db.execute("INSERT INTO revenue (YEAR, MONTH, Total_Revenue) VALUES (?, ?, ?)", year, month, total_price)

    def check_data(self, data):
        col1 = data["Order_ID"]
        col2 = data["Customer_ID"]
        col3 = data["Product_ID"]
        row = db.execute("SELECT Completed FROM jobs WHERE Order_ID = ? AND Customer_ID = ? AND Product_ID = ?", col1, col2, col3)
        complete = int(row[0]["Completed"])
        total = int(data["Quantity"])

        if complete == total:
            return True
        else:
            return False

    def update_data(self, data):
        col1 = data["Order_ID"]
        col2 = data["Customer_ID"]
        col3 = data["Product_ID"]

        db.execute("UPDATE jobs SET Status = 'COMPLETE' WHERE Order_ID = ? AND Customer_ID = ? AND Product_ID = ?", col1, col2, col3)
        db.execute("UPDATE orders SET Status = 'COMPLETE' WHERE Order_ID = ? AND Customer_ID = ? AND Product_ID = ?", col1, col2, col3)
        db.execute("DELETE FROM jobs WHERE  Order_ID = ? AND Customer_ID = ? AND Product_ID = ?", col1, col2, col3)
        self.add_revenue(data)

    def write_data(self, data):
        col1 = data["Order_ID"]
        col2 = data["Customer_ID"]
        col3 = data["Product_ID"]
        db.execute("UPDATE jobs SET Completed = Completed + 1 WHERE Order_ID = ? AND Customer_ID = ? AND Product_ID = ?", col1, col2, col3)

