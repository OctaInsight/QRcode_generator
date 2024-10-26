# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 14:28:43 2024

The owner of this code is Octa Insight

Created by Tamer Abu-Alam - 26.10.2024

@author: tab009
"""

from flask import Flask, request, send_file, render_template
import qrcode
import io

app = Flask(__name__)

# Function to generate the QR code image with specified fill color
def generate_qr_code(url, fill_color="black"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Generate an image with a transparent background
    img = qr.make_image(fill_color=fill_color, back_color=None)
    
    return img

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        fill_color = request.form.get("fill_color", "black")  # Get the color chosen by the user
        img = generate_qr_code(url, fill_color)
        
        # Save the image to a BytesIO stream to send to the user
        img_io = io.BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)
        
        return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="qr_code.png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


""" this is the last working code

import qrcode

def generate_qr_code(url):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image of the QR code
    img = qr.make_image(fill="blue", back_color="white")
    img.save("qr_code.png")
    return "qr_code.png"

# Test the function
url = "https://inspiringtheminds.cloudearthi.com/"
generate_qr_code(url)

"""