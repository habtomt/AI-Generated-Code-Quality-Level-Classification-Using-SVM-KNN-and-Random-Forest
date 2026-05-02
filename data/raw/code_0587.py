"""
Auto-generated Python code
Scenario : SMS & Communication APIs
Prompt   : response_001.txt
Run      : 1
"""

from flask import Flask, request
from twilio.rest import Client
import sqlite3
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)

# Twilio credentials
TWILIO_SID = 'YOUR_TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
TWILIO_PHONE_NUMBER = 'YOUR_TWILIO_PHONE_NUMBER'

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Database setup
def init_db():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS appointments
                 (id INTEGER PRIMARY KEY, customer_name TEXT, phone TEXT, appointment_time DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# Function to schedule an appointment
@app.route('/schedule', methods=['POST'])
def schedule_appointment():
    try:
        customer_name = request.form['customer_name']
        phone = request.form['phone']
        appointment_time_str = request.form['appointment_time']  # Format: YYYY-MM-DD HH:MM:SS
        appointment_time = datetime.strptime(appointment_time_str, '%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('appointments.db')
        c = conn.cursor()
        c.execute("INSERT INTO appointments (customer_name, phone, appointment_time) VALUES (?, ?, ?)",
                  (customer_name, phone, appointment_time))
        conn.commit()
        conn.close()

        return 'Appointment scheduled!'
    except sqlite3.Error as e:
        return f"Error scheduling appointment: {e}"

# Function to send SMS reminders
def send_reminders():
    try:
        conn = sqlite3.connect('appointments.db')
        c = conn.cursor()
        
        # Calculate the time range for reminders
        now = datetime.now()
        reminder_time = now + timedelta(hours=24)
        c.execute("SELECT * FROM appointments WHERE appointment_time BETWEEN ? AND ?", (now, reminder_time))
        
        appointments = c.fetchall()
        for appointment in appointments:
            msg_body = f"Hi {appointment[1]}, this is a reminder for your appointment on {appointment[3]}."
            client.messages.create(
                body=msg_body,
                from_=TWILIO_PHONE_NUMBER,
                to=appointment[2]
            )
        
        conn.close()
    except sqlite3.Error as e:
        print(f"Error sending reminders: {e}")

# Function to initiate reminders every hour
@app.route('/start_reminders', methods=['GET'])
def start_reminder_service():
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=send_reminders, trigger="interval", hours=1)
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())  # Shut down the scheduler at exit
        return "Reminder service started!"
    except Exception as e:
        return f"Error starting reminder service: {e}"

if __name__ == '__main__':
    app.run()