from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageFilter
import io

app = Flask(__name__)

def process_image(image: Image.Image) -> Image.Image:
    image = image.resize((800, 800))
    image = image.filter(ImageFilter.BLUR)
    return image

@app.route("/process-image", methods=["POST"])
def process_image_endpoint():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]

    try:
        img = Image.open(file.stream).convert("RGB")
        processed_img = process_image(img)

        img_io = io.BytesIO()
        processed_img.save(img_io, "JPEG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/jpeg")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)