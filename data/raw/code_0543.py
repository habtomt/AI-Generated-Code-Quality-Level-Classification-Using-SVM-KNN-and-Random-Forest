"""
Auto-generated Python code
Scenario : Payment Processing
Prompt   : response_002.txt
Run      : 1
"""

# Import necessary libraries
import stripe
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize Flask app
app = Flask(__name__)

# Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payment.db'
db = SQLAlchemy(app)

# Initialize Stripe
stripe.api_key = 'YOUR_STRIPE_API_KEY'

# Define models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(100), nullable=False)

# Define schema
ma = Marshmallow(app)

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment

# Initialize schema
customer_schema = CustomerSchema()
payment_schema = PaymentSchema()

# API endpoint to create customer
@app.route('/customers', methods=['POST'])
def create_customer():
    try:
        data = request.json
        customer = Customer(name=data['name'], email=data['email'])
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer_schema.dump(customer))
    except Exception as e:
        return jsonify({'error': str(e)})

# API endpoint to create payment
@app.route('/payments', methods=['POST'])
def create_payment():
    try:
        data = request.json
        customer_id = data['customer_id']
        amount = data['amount']
        payment_method = data['payment_method']
        customer = Customer.query.get(customer_id)
        if customer:
            payment = Payment(customer_id=customer_id, amount=amount, payment_method=payment_method)
            db.session.add(payment)
            db.session.commit()
            # Create payment intent on Stripe
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=[payment_method]
            )
            return jsonify({'payment_intent': intent.id})
        else:
            return jsonify({'error': 'Customer not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

# API endpoint to capture payment
@app.route('/payments/<id>/capture', methods=['POST'])
def capture_payment(id):
    try:
        payment = Payment.query.get(id)
        if payment:
            # Capture payment on Stripe
            payment_capture = stripe.PaymentIntent.capture(
                payment_intent_id=id
            )
            return jsonify({'payment_capture': payment_capture.id})
        else:
            return jsonify({'error': 'Payment not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)