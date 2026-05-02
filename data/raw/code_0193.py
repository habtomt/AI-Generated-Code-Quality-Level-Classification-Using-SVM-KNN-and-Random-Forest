from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <script>
        let cart = JSON.parse(localStorage.getItem('cart')) || [];

        function updateCartUI() {
            localStorage.setItem('cart', JSON.stringify(cart));
            const list = document.getElementById('cart-items');
            list.innerHTML = '';
            let total = 0;
            cart.forEach((item, index) => {
                total += item.price;
                list.innerHTML += `<li>${item.name} - $${item.price} <button onclick="removeItem(${index})">X</button></li>`;
            });
            document.getElementById('total').innerText = total;
        }

        function addItem(name, price) {
            cart.push({name, price});
            updateCartUI();
        }

        function removeItem(index) {
            cart.splice(index, 1);
            updateCartUI();
        }
        window.onload = updateCartUI;
    </script>
</head>
<body>
    <button onclick="addItem('Laptop', 1000)">Add Laptop</button>
    <ul id="cart-items"></ul>
    <p>Total: $<span id="total">0</span></p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)