"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_002.txt
Run      : 3
"""

# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize database
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Define Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Order('{self.id}', '{self.user_id}')"

# Define CheckoutForm
class CheckoutForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    payment_method = StringField('Payment Method', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Define PaymentForm
class PaymentForm(FlaskForm):
    card_number = StringField('Card Number', validators=[DataRequired()])
    expiration_date = StringField('Expiration Date', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create cart
cart = {}

# Route for home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            order = Order(user_id=user.id, items=' '.join(cart.keys()), total=sum(cart.values()), payment_method=form.payment_method.data, payment_status='pending')
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('payment'))
        else:
            user = User(username=form.name.data, email=form.email.data, password=hashlib.sha256(os.urandom(24)).hexdigest(), orders=[order])
            db.session.add(user)
            db.session.commit()
            order = Order(user_id=user.id, items=' '.join(cart.keys()), total=sum(cart.values()), payment_method=form.payment_method.data, payment_status='pending')
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('payment'))
    return render_template('checkout.html', form=form)

# Route for payment page
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    form = PaymentForm()
    if form.validate_on_submit():
        # Simulate payment processing
        # Replace with actual payment gateway API
        payment_status = 'success'
        return render_template('payment_success.html', payment_status=payment_status)
    return render_template('payment.html', form=form)

# Route for adding items to cart
@app.route('/add_to_cart/<item>', methods=['POST'])
def add_to_cart(item):
    if item in cart:
        cart[item] += 1
    else:
        cart[item] = 1
    return redirect(url_for('home'))

# Route for removing items from cart
@app.route('/remove_from_cart/<item>', methods=['POST'])
def remove_from_cart(item):
    if item in cart:
        del cart[item]
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)