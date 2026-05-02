"""
Auto-generated Python code
Scenario : Email Sending - Email Marketing
Prompt   : response_002.txt
Run      : 3
"""

# Import required libraries
import os
import time
from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = "YOUR_EMAIL@gmail.com"
PASSWORD = "YOUR_PASSWORD"

# Database credentials
DB_HOST = "localhost"
DB_USER = "YOUR_USER"
DB_PASSWORD = "YOUR_PASSWORD"
DB_NAME = "YOUR_DB"

# API credentials (e.g., for product recommendations)
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

# Set up database connection
import mysql.connector
cnx = mysql.connector.connect(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME
)

# Create a cursor object
cursor = cnx.cursor()

# Define a function to get the cart abandonment data
def get_cart_abandonment_data():
    query = """
        SELECT *
        FROM orders
        WHERE status = 'abandoned'
    """
    cursor.execute(query)
    return cursor.fetchall()

# Define a function to train a model for product recommendations
def train_recommendation_model():
    # Load the product data
    query = """
        SELECT *
        FROM products
    """
    cursor.execute(query)
    product_data = cursor.fetchall()

    # Create a DataFrame from the product data
    products_df = pd.DataFrame(product_data)

    # Define the feature columns
    feature_cols = ['product_name', 'description']

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer to the feature columns and transform the data
    vectorized_data = vectorizer.fit_transform(products_df[feature_cols])

    # Define the label column
    label_col = 'category'

    # Use a LabelEncoder to encode the labels
    le = LabelEncoder()
    products_df[label_col] = le.fit_transform(products_df[label_col])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(vectorized_data, products_df[label_col], test_size=0.2, random_state=42)

    # Define a random forest classifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42)

    # Define a logistic regression classifier
    lr = LogisticRegression(max_iter=1000)

    # Define a grid search for hyperparameter tuning
    param_grid = {
        'n_estimators': [10, 50, 100],
        'max_depth': [None, 5, 10],
        'min_samples_split': [2, 5, 10]
    }

    # Perform a grid search for the random forest classifier
    grid_search_rf = GridSearchCV(rf, param_grid, cv=5, scoring='accuracy')
    grid_search_rf.fit(X_train, y_train)

    # Perform a grid search for the logistic regression classifier
    grid_search_lr = GridSearchCV(lr, param_grid, cv=5, scoring='accuracy')
    grid_search_lr.fit(X_train, y_train)

    # Evaluate the models
    print("Random Forest Model:")
    print(classification_report(y_test, grid_search_rf.predict(X_test)))
    print("Logistic Regression Model:")
    print(classification_report(y_test, grid_search_lr.predict(X_test)))

    # Save the best models to files
    with open('rf_best_model.pkl', 'wb') as f:
        pickle.dump(grid_search_rf.best_estimator_, f)
    with open('lr_best_model.pkl', 'wb') as f:
        pickle.dump(grid_search_lr.best_estimator_, f)

# Define a function to get personalized product recommendations
def get_recommendations(user_id):
    # Load the best model
    with open('rf_best_model.pkl', 'rb') as f:
        model = pickle.load(f)

    # Get the user's cart data
    query = """
        SELECT *
        FROM carts
        WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    cart_data = cursor.fetchall()

    # Create a DataFrame from the cart data
    cart_df = pd.DataFrame(cart_data)

    # Get the product IDs from the cart
    product_ids = cart_df['product_id'].tolist()

    # Get the product data
    query = """
        SELECT *
        FROM products
        WHERE id IN (%s)
    """
    cursor.execute(query, ','.join(map(str, product_ids)))
    product_data = cursor.fetchall()

    # Create a DataFrame from the product data
    products_df = pd.DataFrame(product_data)

    # Define the feature columns
    feature_cols = ['product_name', 'description']

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer to the feature columns and transform the data
    vectorized_data = vectorizer.fit_transform(products_df[feature_cols])

    # Get the recommendations
    recommendations = model.predict(vectorized_data)

    # Return the recommendations as a list of product IDs
    return recommendations.tolist()

# Define a function to send follow-up emails
def send_follow_up_emails():
    # Get the cart abandonment data
    cart_abandonment_data = get_cart_abandonment_data()

    # Create a DataFrame from the cart abandonment data
    cart_abandonment_df = pd.DataFrame(cart_abandonment_data)

    # Get the user IDs and order IDs
    user_ids = cart_abandonment_df['user_id'].unique()
    order_ids = cart_abandonment_df['order_id'].unique()

    # Loop through the user IDs and order IDs
    for user_id in user_ids:
        for order_id in order_ids:
            # Get the cart data for the user and order
            query = """
                SELECT *
                FROM carts
                WHERE user_id = %s AND order_id = %s
            """
            cursor.execute(query, (user_id, order_id))
            cart_data = cursor.fetchall()

            # Create a DataFrame from the cart data
            cart_df = pd.DataFrame(cart_data)

            # Get the product IDs from the cart
            product_ids = cart_df['product_id'].tolist()

            # Get the product data
            query = """
                SELECT *
                FROM products
                WHERE id IN (%s)
            """
            cursor.execute(query, ','.join(map(str, product_ids)))
            product_data = cursor.fetchall()

            # Create a DataFrame from the product data
            products_df = pd.DataFrame(product_data)

            # Get the recommendations
            recommendations = get_recommendations(user_id)

            # Create a message
            message = MIMEMultipart()
            message['From'] = FROM_EMAIL
            message['To'] = 'user@example.com'
            message['Subject'] = 'Follow-up Email'

            # Create the body of the message
            body = """
                Dear User,

                We noticed that you abandoned your cart with order ID %s. We want to follow up with you to see if you need any help with your purchase.

                We recommend the following products:

                """ % order_id
            for recommendation in recommendations:
                product_name = products_df.loc[products_df['id'] == recommendation, 'name'].iloc[0]
                body += '%s\n' % product_name

            # Attach the body to the message
            message.attach(MIMEText(body, 'plain'))

            # Send the email
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(FROM_EMAIL, PASSWORD)
            server.sendmail(FROM_EMAIL, 'user@example.com', message.as_string())
            server.quit()

# Define a function to trigger follow-up emails
def trigger_follow_up_emails():
    # Get the cart abandonment data
    cart_abandonment_data = get_cart_abandonment_data()

    # Create a DataFrame from the cart abandonment data
    cart_abandonment_df = pd.DataFrame(cart_abandonment_data)

    # Get the user IDs and order IDs
    user_ids = cart_abandonment_df['user_id'].unique()
    order_ids = cart_abandonment_df['order_id'].unique()

    # Loop through the user IDs and order IDs
    for user_id in user_ids:
        for order_id in order_ids:
            # Check if the order is more than 24 hours old
            query = """
                SELECT *
                FROM orders
                WHERE id = %s AND status = 'abandoned' AND created_at < NOW() - INTERVAL 24 HOUR
            """
            cursor.execute(query, (order_id,))
            if cursor.fetchone():
                # Send a follow-up email
                send_follow_up_emails()

# Trigger follow-up emails every 24 hours
while True:
    trigger_follow_up_emails()
    time.sleep(24 * 60 * 60)

# Close the database connection
cnx.close()