"""
Auto-generated Python code
Scenario : E-commerce
Prompt   : response_002.txt
Run      : 2
"""

# Import necessary libraries
import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import stripe

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['STRIPE_PUBLIC_KEY'] = 'YOUR_STRIPE_PUBLIC_KEY'
app.config['STRIPE_SECRET_KEY'] = 'YOUR_STRIPE_SECRET_KEY'

# Initialize database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

# Initialize Stripe API
stripe.api_key = 'YOUR_STRIPE_SECRET_KEY'

# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_guest = db.Column(db.Boolean, nullable=False, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Define Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)

# Define form for registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# Define form for login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Define form for checkout
class CheckoutForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    submit = SubmitField('Place Order')

# Define route for home page
@app.route('/')
def home():
    return render_template('home.html')

# Define route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

# Define route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Define route for checkout page
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        try:
            # Create Stripe customer
            customer = stripe.Customer.create(
                email=form.email.data,
                name=form.name.data,
                address=form.address.data,
                city=form.city.data,
                state=form.state.data,
                zip=form.zip_code.data
            )
            
            # Create Stripe payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=1000,
                currency='usd',
                payment_method_types=['card']
            )
            
            # Create order
            order = Order(user_id=current_user.id, total=1000, payment_status='pending')
            db.session.add(order)
            db.session.commit()
            
            # Redirect to payment page
            return redirect(url_for('payment', payment_intent=payment_intent.id, customer_id=customer.id))
        except Exception as e:
            print(str(e))
    return render_template('checkout.html', form=form)

# Define route for payment page
@app.route('/payment/<payment_intent>/<customer_id>', methods=['GET', 'POST'])
@login_required
def payment(payment_intent, customer_id):
    form = CheckoutForm()
    if form.validate_on_submit():
        try:
            # Confirm Stripe payment intent
            stripe.PaymentIntent.confirm(payment_intent)
            
            # Update order status
            order = Order.query.filter_by(user_id=current_user.id, payment_status='pending').first()
            order.payment_status = 'paid'
            db.session.commit()
            
            # Log out user
            logout_user()
            return redirect(url_for('home'))
        except Exception as e:
            print(str(e))
    return render_template('payment.html', form=form)

# Define route for guest checkout
@app.route('/guest_checkout', methods=['GET', 'POST'])
def guest_checkout():
    try:
        # Create Stripe customer
        customer = stripe.Customer.create(
            email='guest@example.com',
            name='Guest'
        )
        
        # Create Stripe payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=1000,
            currency='usd',
            payment_method_types=['card']
        )
        
        # Create order
        order = Order(total=1000, payment_status='pending')
        db.session.add(order)
        db.session.commit()
        
        # Redirect to payment page
        return redirect(url_for('guest_payment', payment_intent=payment_intent.id, customer_id=customer.id))
    except Exception as e:
        print(str(e))

# Define route for guest payment page
@app.route('/guest_payment/<payment_intent>/<customer_id>', methods=['GET', 'POST'])
def guest_payment(payment_intent, customer_id):
    form = CheckoutForm()
    if form.validate_on_submit():
        try:
            # Confirm Stripe payment intent
            stripe.PaymentIntent.confirm(payment_intent)
            
            # Update order status
            order = Order.query.filter_by(payment_status='pending').first()
            order.payment_status = 'paid'
            db.session.commit()
            
            # Log out user
            return redirect(url_for('home'))
        except Exception as e:
            print(str(e))
    return render_template('payment.html', form=form)

# Run app
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)