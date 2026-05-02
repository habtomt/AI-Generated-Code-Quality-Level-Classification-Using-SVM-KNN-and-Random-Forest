from flask import Flask, session, request, redirect, url_for, render_template_string, jsonify

app = Flask(__name__)
app.secret_key = "dev_secret_key"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Checkout</title>
</head>
<body>
    <h2>Checkout Process</h2>

    <div>
        <p>Step: {{ step }} / 3</p>
        <progress value="{{ step }}" max="3"></progress>
    </div>

    {% if step == 1 %}
    <h3>Cart</h3>
    <form method="POST" action="/step1">
        <label>Item Name:</label>
        <input name="item" required>
        <label>Quantity:</label>
        <input name="qty" type="number" min="1" required>
        <button type="submit">Continue</button>
    </form>

    {% elif step == 2 %}
    <h3>Shipping Info</h3>
    <form method="POST" action="/step2">
        <label>Name:</label>
        <input name="name" required>
        <label>Address:</label>
        <input name="address" required>
        <button type="submit">Continue</button>
    </form>

    {% elif step == 3 %}
    <h3>Payment</h3>
    <form method="POST" action="/step3">
        <label>Card Number:</label>
        <input name="card" required>
        <label>CVV:</label>
        <input name="cvv" required>
        <button type="submit">Pay</button>
    </form>

    {% elif step == 4 %}
    <h3>Success</h3>
    <p>Order completed successfully!</p>
    <a href="/reset">New Order</a>
    {% endif %}

</body>
</html>
"""

@app.route("/")
def index():
    session["step"] = 1
    session["data"] = {}
    return redirect(url_for("step"))

@app.route("/step", methods=["GET"])
def step():
    return render_template_string(HTML, step=session.get("step", 1))

@app.route("/step1", methods=["POST"])
def step1():
    item = request.form.get("item")
    qty = request.form.get("qty")

    if not item or not qty.isdigit() or int(qty) <= 0:
        return "Invalid cart data", 400

    session["data"]["cart"] = {"item": item, "qty": int(qty)}
    session["step"] = 2
    return redirect(url_for("step"))

@app.route("/step2", methods=["POST"])
def step2():
    name = request.form.get("name")
    address = request.form.get("address")

    if not name or not address:
        return "Invalid shipping data", 400

    session["data"]["shipping"] = {"name": name, "address": address}
    session["step"] = 3
    return redirect(url_for("step"))

@app.route("/step3", methods=["POST"])
def step3():
    card = request.form.get("card")
    cvv = request.form.get("cvv")

    if not card or not cvv or len(cvv) < 3:
        return "Payment validation failed", 400

    if not card.isdigit():
        return "Invalid card", 400

    session["data"]["payment"] = {"card": "****" + card[-4:]}
    session["step"] = 4
    return redirect(url_for("step"))

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)