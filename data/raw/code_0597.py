"""
Auto-generated Python code
Scenario : SMS & Communication APIs
Prompt   : response_001.txt
Run      : 3
"""

# Import necessary libraries
import twilio
from datetime import datetime, timedelta
import schedule
import time

# Twilio Account Credentials
ACCOUNT_SID = 'YOUR_ACCOUNT_SID'
AUTH_TOKEN = 'YOUR_AUTH_TOKEN'
SMS_GATEWAY_PHONE_NUMBER = 'YOUR_SMS_GATEWAY_PHONE_NUMBER'

# Database Credentials
DB_HOST = 'YOUR_DB_HOST'
DB_USER = 'YOUR_DB_USER'
DB_PASSWORD = 'YOUR_DB_PASSWORD'
DB_NAME = 'YOUR_DB_NAME'

# SQL Query to fetch upcoming appointments
fetch_upcoming_appointments_query = """
    SELECT customer_name, appointment_date, appointment_time, customer_phone_number
    FROM appointments
    WHERE appointment_date >= CURRENT_DATE AND appointment_status = 'pending'
"""

# Function to send SMS reminders
def send_sms_reminders():
    try:
        # Import Twilio library
        client = twilio.rest.Client(ACCOUNT_SID, AUTH_TOKEN)
        
        # Connect to database
        import mysql.connector
        cnx = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME
        )
        
        # Fetch upcoming appointments
        cursor = cnx.cursor()
        cursor.execute(fetch_upcoming_appointments_query)
        upcoming_appointments = cursor.fetchall()
        
        # Send SMS reminders for each upcoming appointment
        for appointment in upcoming_appointments:
            customer_name = appointment[0]
            appointment_date = appointment[1]
            appointment_time = appointment[2]
            customer_phone_number = appointment[3]
            
            # Calculate time difference between current time and appointment time
            current_time = datetime.now().strftime("%H:%M")
            appointment_time_diff = (datetime.strptime(appointment_time, '%Y-%m-%d %H:%M') - datetime.now()).total_seconds() / 3600
            
            # Send SMS reminder 6 hours prior to appointment time
            if appointment_time_diff >= 6:
                message = client.messages.create(
                    body=f"Reminder: Your appointment with {customer_name} is scheduled for {appointment_date} at {appointment_time}.",
                    from_=SMS_GATEWAY_PHONE_NUMBER,
                    to=customer_phone_number
                )
                print(f"SMS reminder sent to {customer_phone_number}: {message.sid}")
        
        # Close database connection
        cursor.close()
        cnx.close()
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    except twilio.base.exceptions.TwilioRestException as e:
        print(f"Error: {e}")

# Schedule send_sms_reminders function to run daily at 8:00 AM
schedule.every().day.at("08:00").do(send_sms_reminders)

# Run scheduled task
while True:
    schedule.run_pending()
    time.sleep(1)