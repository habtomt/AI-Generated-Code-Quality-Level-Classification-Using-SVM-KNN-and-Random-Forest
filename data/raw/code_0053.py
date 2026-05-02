import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import time

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@example.com"
SENDER_PASSWORD = "your_password"

ABANDONMENT_THRESHOLD_MINUTES = 30

USERS_FILE = "users.csv"
CART_FILE = "carts.csv"
PRODUCTS_FILE = "products.csv"

def load_data():
    users = pd.read_csv(USERS_FILE)
    carts = pd.read_csv(CART_FILE)
    products = pd.read_csv(PRODUCTS_FILE)
    return users, carts, products

def get_recommendations(cart_items, products_df):
    recommendations = []
    for item in cart_items:
        matches = products_df[products_df["category"] == item["category"]]
        recommendations.extend(matches["product_name"].head(2).tolist())
    return list(set(recommendations))[:3]

def build_email(user_name, cart_items, recommendations):
    items_text = "\n".join([f"- {i['product_name']}" for i in cart_items])
    rec_text = "\n".join([f"- {r}" for r in recommendations])

    body = f"""
Hi {user_name},

We noticed you left some items in your cart:

{items_text}

You might also like:
{rec_text}

Complete your purchase now before items sell out!

Best regards,
Your Store Team
"""
    return body

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"Sent email to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def detect_abandoned_carts(carts_df):
    now = datetime.now()
    abandoned = []

    for _, row in carts_df.iterrows():
        last_update = datetime.strptime(row["last_activity"], "%Y-%m-%d %H:%M:%S")
        if now - last_update > timedelta(minutes=ABANDONMENT_THRESHOLD_MINUTES):
            abandoned.append(row)

    return abandoned

def process_abandoned_carts():
    users, carts, products = load_data()
    abandoned_carts = detect_abandoned_carts(carts)

    for cart in abandoned_carts:
        user = users[users["user_id"] == cart["user_id"]].iloc[0]

        cart_items = eval(cart["items"])
        recommendations = get_recommendations(cart_items, products)

        email_body = build_email(
            user["name"],
            cart_items,
            recommendations
        )

        send_email(user["email"], "You left something behind!", email_body)

def main():
    while True:
        process_abandoned_carts()
        time.sleep(300)

if __name__ == "__main__":
    main()