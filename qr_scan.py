from datetime import datetime
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time

class QRScanner:
    def __init__(self):
        self.cap = None

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
                    product_id = obj.data.decode('utf-8')

                    # Check if the specified delay has passed since the last processed QR code
                    current_time = time.time()
                    if current_time - last_process_time >= delay_between_scans:
                        last_process_time = current_time

                        # Get the current timestamp
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        # Do something with the QR code data and timestamp (e.g., print them)
                        print(f"Scanned QR Code: {product_id} | Timestamp: {timestamp}")

                        # Display the QR code data and timestamp on the frame
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        bottom_left_corner = (pts[0][0], pts[0][1] - 10)
                        font_scale = 0.5
                        font_color = (255, 255, 255)
                        line_type = 1
                        cv2.putText(frame, f"ID: {product_id} | Time: {timestamp}", bottom_left_corner, font, font_scale, font_color, line_type)

                        # Segregate the timestamp components
                        year, month, day, hour, minute, second = self.segregate_timestamp(timestamp)
                        print(f"Year: {year}, Month: {month}, Day: {day}, Hour: {hour}, Minute: {minute}, Second: {second}")

            # Display the frame with the rectangles around the QR codes
            cv2.imshow("QR Code Scanner", frame)

            # Press 'Esc' to exit
            if cv2.waitKey(1) & 0xFF == 27:
                break

    def stop_scanner(self):
        if self.cap is not None:
            self.cap.release()
            cv2.destroyAllWindows()