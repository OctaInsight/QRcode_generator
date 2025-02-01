# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 14:28:43 2024

The owner of this code is Octa Insight

Created by Tamer Abu-Alam - 26.10.2024
Modified in Feb. 1, 2025

@author: tab009
"""
import streamlit as st
import qrcode
import io
from PIL import Image, ImageDraw

# Define QR code sizes
QR_SIZES = {
    "Small": 150,
    "Medium": 250,
    "Large": 400,
    "Extra Large": 600,
    "Custom": None  # User-defined size
}

# Function to generate QR code with a predefined center square
def generate_qr_code(url, fill_color="black", logo=None, output_format="PNG", transparent=False, qr_size=250):
    qr = qrcode.QRCode(
        version=5,  
        error_correction=qrcode.constants.ERROR_CORRECT_H,  
        box_size=qr_size // 41,  
        border=2,  
    )
    qr.add_data(url)
    qr.make(fit=True)

    back_color = "white" if not transparent else None  
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

    img_w, img_h = img.size

    square_size = int(img_w * 0.2)

    draw = ImageDraw.Draw(img)
    square_position = ((img_w - square_size) // 2, (img_h - square_size) // 2, 
                       (img_w + square_size) // 2, (img_h + square_size) // 2)
    draw.rectangle(square_position, fill="white")  

    if logo:
        logo = Image.open(logo).convert("RGBA")

        max_logo_size = square_size * 0.9  
        logo_w, logo_h = logo.size
        scale_factor = min(max_logo_size / logo_w, max_logo_size / logo_h)

        if scale_factor < 1:
            new_size = (int(logo_w * scale_factor), int(logo_h * scale_factor))
            logo = logo.resize(new_size, Image.LANCZOS)

        pos = ((img_w - logo.size[0]) // 2, (img_h - logo.size[1]) // 2)
        img.paste(logo, pos, mask=logo)

    img_io = io.BytesIO()
    img.save(img_io, format=output_format)  
    img_io.seek(0)

    return img_io

# Streamlit UI
st.title("QR Code Generator with Center Space for Product Image")

url = st.text_input("Enter the URL or text:")

color = st.color_picker("Choose QR Code Color", "#000000")  

uploaded_logo = st.file_uploader("Upload a product image (optional, PNG format)", type=["png", "jpg"])

file_format = st.selectbox("Choose file format", ["PNG", "PNG (Transparent Background)"])  # Removed JPEG

qr_size_choice = st.selectbox("Choose QR Code Size", list(QR_SIZES.keys()), index=1)  
if qr_size_choice == "Custom":
    qr_size = st.number_input("Enter custom QR code size (px):", min_value=100, max_value=1000, value=250, step=50)
else:
    qr_size = QR_SIZES[qr_size_choice]

if url:
    transparent = True if file_format == "PNG (Transparent Background)" else False
    output_format = "PNG"  # Default format is PNG

    img_bytes = generate_qr_code(url, fill_color=color, logo=uploaded_logo, output_format=output_format, transparent=transparent, qr_size=qr_size)

    img_display = Image.open(img_bytes)
    st.image(img_display, caption="Generated QR Code", width=qr_size)  

    st.download_button(
        label=f"Download QR Code ({file_format})",
        data=img_bytes,
        file_name=f"qr_code.{file_format.lower().replace(' ', '_')}",
        mime="image/png"
    )
