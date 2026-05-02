import io
from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageFilter

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    """
    HTTP Trigger to process and analyze images.
    Expects an image file in the request body (multipart/form-data).
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    
    try:
        # Open the image using Pillow (PIL)
        img = Image.open(file.stream)

        # --- Image Processing ---
        
        # 1. Resize: Maintain aspect ratio or force dimensions
        processed_img = img.resize((800, 600))

        # 2. Filter: Apply a blur filter for analysis/preprocessing
        processed_img = processed_img.filter(ImageFilter.GaussianBlur(radius=2))

        # 3. Grayscale: Convert for simpler analysis
        processed_img = processed_img.convert('L')

        # --- Analysis Metadata ---
        analysis = {
            "format": img.format,
            "original_size": img.size,
            "processed_size": processed_img.size,
            "mode": img.mode
        }

        # Save to memory buffer to return via HTTP
        img_io = io.BytesIO()
        processed_img.save(img_io, 'JPEG', quality=85)
        img_io.seek(0)

        return send_file(
            img_io, 
            mimetype='image/jpeg',
            download_name='processed_image.jpg'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)