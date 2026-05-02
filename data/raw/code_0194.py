from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/checkout/validate', methods=['POST'])
def validate_step():
    step = request.json.get('step')
    data = request.json.get('data')
    
    if step == 1: # Shipping
        if not data.get('address'):
            return jsonify({"status": "error", "message": "Address required"}), 400
    elif step == 2: # Payment
        if len(data.get('card', '')) < 16:
            return jsonify({"status": "error", "message": "Invalid card"}), 400
            
    return jsonify({"status": "success", "next_step": step + 1})

@app.route('/checkout/process', methods=['POST'])
def process_payment():
    # Mocking secure payment processing
    return jsonify({"status": "complete", "order_id": "TXN12345"})

if __name__ == "__main__":
    app.run(debug=True)