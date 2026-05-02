from flask import Flask, render_template_string, jsonify, request
import random

app = Flask(__name__)

products = {
    1: {"name": "Tech Gadget", "base_price": 100, "desc": "High-performance device."},
    2: {"name": "Smart Watch", "base_price": 250, "desc": "Track your health metrics."},
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Dynamic Store</title>
    <script>
        function updatePrice(id) {
            fetch(`/api/price/${id}`)
                .then(res => res.json())
                .then(data => {
                    document.getElementById(`price-${id}`).innerText = `$${data.price}`;
                });
        }
        function loadDetails(id) {
            fetch(`/api/details/${id}`)
                .then(res => res.json())
                .then(data => {
                    document.getElementById(`desc-${id}`).innerText = data.description;
                });
        }
        setInterval(() => { [1,2].forEach(updatePrice); }, 5000);
    </script>
</head>
<body>
    <div id="product-1">
        <h2 onclick="loadDetails(1)">Tech Gadget (Click for Details)</h2>
        <p id="price-1">$100</p>
        <p id="desc-1"></p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/price/<int:pid>')
def get_price(pid):
    new_price = products[pid]['base_price'] + random.randint(-5, 5)
    return jsonify({"price": new_price})

@app.route('/api/details/<int:pid>')
def get_details(pid):
    return jsonify({"description": products[pid]['desc'] + " Built with latest tech."})

if __name__ == "__main__":
    app.run(debug=True)