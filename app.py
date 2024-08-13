from flask import Flask, render_template, request, jsonify, send_file
import os
from PIL import Image
import io
import json

app = Flask(__name__)

# Load the themes
with open('assets/themes.json') as f:
    themes = json.load(f)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image upload and conversion
@app.route('/convert', methods=['POST'])
def convert_image():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        theme_name = request.form.get('theme')
        theme = themes.get(theme_name)

        # Load the image
        img = Image.open(file.stream)
        img = img.convert("RGB")
        
        # Convert the image to the selected palette
        converted_img = convert_to_palette(img, theme)

        # Save the converted image to a byte stream
        byte_io = io.BytesIO()
        converted_img.save(byte_io, 'PNG')
        byte_io.seek(0)
        
        return send_file(byte_io, mimetype='image/png')

# Function to convert an image to a specific palette
def convert_to_palette(image, palette):
    pixels = list(image.getdata())
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel
        closest_color = min(palette, key=lambda color: (r - color[0])**2 + (g - color[1])**2 + (b - color[2])**2)
        new_pixels.append(tuple(closest_color))
    
    new_image = Image.new("RGB", image.size)
    new_image.putdata(new_pixels)
    return new_image

if __name__ == '__main__':
    app.run(debug=True)
