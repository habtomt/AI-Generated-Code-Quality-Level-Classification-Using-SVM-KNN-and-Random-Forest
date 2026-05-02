import smtplib
import uuid
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@example.com"
SENDER_PASSWORD = "your_password"

SUBSCRIBERS_FILE = "subscribers.csv"

def load_subscribers():
    try:
        return pd.read_csv(SUBSCRIBERS_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["email", "name", "token", "confirmed", "preferences"])

def save_subscribers(df):
    df.to_csv(SUBSCRIBERS_FILE, index=False)

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
    server.quit()

def send_confirmation_email(email, name, token):
    link = f"http://localhost:5000/confirm?token={token}"
    body = f"""
Hi {name},

Please confirm your newsletter subscription by clicking the link below:

{link}

You can also manage your preferences after confirmation.

"""
    send_email(email, "Confirm your subscription", body)

def subscribe_user(name, email):
    df = load_subscribers()

    if email in df["email"].values:
        return

    token = str(uuid.uuid4())

    new_user = {
        "email": email,
        "name": name,
        "token": token,
        "confirmed": False,
        "preferences": "all"
    }

    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    save_subscribers(df)

    send_confirmation_email(email, name, token)

def confirm_subscription(token):
    df = load_subscribers()

    if token not in df["token"].values:
        return "Invalid token"

    df.loc[df["token"] == token, "confirmed"] = True
    save_subscribers(df)
    return "Subscription confirmed"

def update_preferences(token, preferences):
    df = load_subscribers()

    if token not in df["token"].values:
        return "Invalid token"

    df.loc[df["token"] == token, "preferences"] = preferences
    save_subscribers(df)
    return "Preferences updated"

if __name__ == "__main__":
    subscribe_user("John Doe", "john@example.com")