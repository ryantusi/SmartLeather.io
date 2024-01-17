import qrcode
import os
import json

def generate_qr_code(data_dict):

    # Generate a simple QR ID using a passcode to access database for QR ID counter
    qr_id = data_dict["Order_ID"]
    print(data_dict)

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data_dict)

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add JSON data to the QR code
    qr.add_data(json_data)
    qr.make(fit=True)

    # Create an image from the QR code instance
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image with the unique QR ID as the filename
    qr_filename = f"static/QR_codes/{qr_id}.png"
    qr_image.save(qr_filename)


# Example usage:
if __name__ == "__main__":
    data_to_encode = {
    "product_name": "loafers",
    "product_id": 101,
    "price": 100,
    "QR_ID": "QR101"
    }
    
    
