# cart_recovery.py
from email.message import EmailMessage

def trigger_abandoned_cart_email(user_data, cart_items):
    recommendations = ", ".join([item['name'] for item in cart_items[:2]])
    
    msg = EmailMessage()
    body = f"Hi {user_data['name']},\nYou left something behind! Based on your cart, you might also like {recommendations}."
    msg.set_content(body)
    msg['Subject'] = "Complete your purchase"
    msg['To'] = user_data['email']
    
    print(f"Recovery email triggered for {user_data['email']}")

user = {'name': 'Dana', 'email': 'dana@example.com'}
cart = [{'name': 'Laptop'}, {'name': 'Mouse'}]

if __name__ == "__main__":
    trigger_abandoned_cart_email(user, cart)