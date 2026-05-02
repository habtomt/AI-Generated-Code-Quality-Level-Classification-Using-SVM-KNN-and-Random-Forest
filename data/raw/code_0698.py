"""
Auto-generated Python code
Scenario : Voice & Video Communication
Prompt   : response_003.txt
Run      : 2
"""

```python
# Import necessary libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cv2
from cv2 import VideoCapture, imshow, waitKey, destroyAllWindows
import numpy as np
import socket
import select
import threading
import sqlite3
from sqlite3 import Error
import ssl
import base64
import hashlib
import hmac
import os

# Create a SQLite database
def create_db():
    conn = None
    try:
        conn = sqlite3.connect('telemedicine.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, password TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS appointments
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, date TEXT, time TEXT, status TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS medical_records
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, record TEXT)''')
        conn.commit()
        conn.close()
    except Error as e:
        print(e)

# Create a secure socket
def create_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain('server.crt', 'server.key')
    context.load_verify_locations('client.crt')
    context.verify_mode = ssl.CERT_REQUIRED
    server_socket = context.wrap_socket(server_socket, server_side=True)
    return server_socket

# Handle incoming connections
def handle_client(client_socket, address):
    try:
        # Receive data from client
        data = client_socket.recv(1024)
        if not data:
            return
        # Authenticate client
        auth_response = authenticate(data.decode('utf-8'))
        if auth_response:
            # Handle video call
            handle_video_call(client_socket, address)
        else:
            # Handle authentication failure
            client_socket.send('Authentication failed'.encode('utf-8'))
            client_socket.close()
    except Exception as e:
        print(f'Error handling client: {e}')

# Authenticate client
def authenticate(data):
    # Extract username and password
    username, password = data.split(':')
    # Query database for username and password
    conn = sqlite3.connect('telemedicine.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return True
    else:
        return False

# Handle video call
def handle_video_call(client_socket, address):
    # Receive video frames from client
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        # Send video frames to client
        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        client_socket.send(base64.b64encode(frame_bytes))
        # Receive video frames from client
        data = client_socket.recv(1024)
        if not data:
            break
    video_capture.release()
    client_socket.close()

# Create a GUI for appointment scheduling
class AppointmentScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title('Appointment Scheduler')
        self.root.geometry('400x200')
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        self.notebook.add(ttk.Frame(self.notebook), text='Schedule Appointment')
        self.notebook.add(ttk.Frame(self.notebook), text='View Appointments')
        self.schedule_frame = self.notebook.tabs()[0]
        self.view_frame = self.notebook.tabs()[1]
        self.schedule_appointment()

    def schedule_appointment(self):
        # Create labels and entries for user input
        self.label1 = ttk.Label(self.schedule_frame, text='User ID:')
        self.label1.pack()
        self.entry1 = ttk.Entry(self.schedule_frame)
        self.entry1.pack()
        self.label2 = ttk.Label(self.schedule_frame, text='Date:')
        self.label2.pack()
        self.entry2 = ttk.Entry(self.schedule_frame)
        self.entry2.pack()
        self.label3 = ttk.Label(self.schedule_frame, text='Time:')
        self.label3.pack()
        self.entry3 = ttk.Entry(self.schedule_frame)
        self.entry3.pack()
        # Create button to schedule appointment
        self.button1 = ttk.Button(self.schedule_frame, text='Schedule Appointment', command=self.schedule)
        self.button1.pack()

    def schedule(self):
        # Get user input
        user_id = self.entry1.get()
        date = self.entry2.get()
        time = self.entry3.get()
        # Schedule appointment
        conn = sqlite3.connect('telemedicine.db')
        c = conn.cursor()
        c.execute("INSERT INTO appointments (user_id, date, time) VALUES (?, ?, ?)", (user_id, date, time))
        conn.commit()
        conn.close()
        # Display success message
        messagebox.showinfo('Appointment Scheduled', 'Appointment scheduled successfully')

    def view_appointments(self):
        # Create label to display appointments
        self.label4 = ttk.Label(self.view_frame, text='Appointments:')
        self.label4.pack()
        # Get appointments from database
        conn = sqlite3.connect('telemedicine.db')
        c = conn.cursor()
        c.execute("SELECT * FROM appointments")
        appointments = c.fetchall()
        conn.close()
        # Display appointments
        for appointment in appointments:
            self.label5 = ttk.Label(self.view_frame, text=f'User ID: {appointment[1]}, Date: {appointment[2]}, Time: {appointment[3]}')
            self.label5.pack()

# Create a GUI for medical record sharing
class MedicalRecordShare:
    def __init__(self, root):
        self.root = root
        self.root.title('Medical Record Share')
        self.root.geometry('400x200')
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        self.notebook.add(ttk.Frame(self.notebook), text='Share Medical Record')
        self.notebook.add(ttk.Frame(self.notebook), text='View Medical Records')
        self.share_frame = self.notebook.tabs()[0]
        self.view_frame = self.notebook.tabs()[1]
        self.share_medical_record()

    def share_medical_record(self):
        # Create labels and entries for user input
        self.label6 = ttk.Label(self.share_frame, text='User ID:')
        self.label6.pack()
        self.entry4 = ttk.Entry(self.share_frame)
        self.entry4.pack()
        self.label7 = ttk.Label(self.share_frame, text='Medical Record:')
        self.label7.pack()
        self.entry5 = ttk.Entry(self.share_frame)
        self.entry5.pack()
        # Create button to share medical record
        self.button2 = ttk.Button(self.share_frame, text='Share Medical Record', command=self.share)
        self.button2.pack()

    def share(self):
        # Get user input
        user_id = self.entry4.get()
        medical_record = self.entry5.get()
        # Share medical record
        conn = sqlite3.connect('telemedicine.db')
        c = conn.cursor()
        c.execute("INSERT INTO medical_records (user_id, record) VALUES (?, ?)", (user_id, medical_record))
        conn.commit()
        conn.close()
        # Display success message
        messagebox.showinfo('Medical Record Shared', 'Medical record shared successfully')

    def view_medical_records(self):
        # Create label to display medical records
        self.label8 = ttk.Label(self.view_frame, text='Medical Records:')
        self.label8.pack()
        # Get medical records from database
        conn = sqlite3.connect('telemedicine.db')
        c = conn.cursor()
        c.execute("SELECT * FROM medical_records")
        medical_records = c.fetchall()
        conn.close()
        # Display medical records
        for medical_record in medical_records:
            self.label9 = ttk.Label(self.view_frame, text=f'User ID: {medical_record[1]}, Record: {medical_record[2]}')
            self.label9.pack()

# Create a GUI for telemedicine system
class TelemedicineSystem:
    def __init__(self, root):
        self.root = root
        self.root.title('Telemedicine System')
        self.root.geometry('400x200')
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        self.notebook.add(ttk.Frame(self.notebook), text='Schedule Appointment')
        self.notebook.add(ttk.Frame(self.notebook), text='Share Medical Record')
        self.schedule_appointment_frame = self.notebook.tabs()[0]
        self.share_medical_record_frame = self.notebook.tabs()[1]
        self.schedule_appointment()
        self.share_medical_record()

    def schedule_appointment(self):
        # Create an instance of the appointment scheduler
        self.appointment_scheduler = AppointmentScheduler(self.schedule_appointment_frame)

    def share_medical_record(self):
        # Create an instance of the medical record share
        self.medical_record_share = MedicalRecordShare(self.share_medical_record_frame)

# Create a server
if __name__ == '__main__':
    create_db()
    server_socket = create_socket()
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print('Server is listening on port 12345')
    # Handle incoming connections
    while True:
        client_socket, address = server_socket.accept()
        print(f'Incoming connection from {address}')
        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args