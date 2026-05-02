import datetime
import time

class AppointmentReminderSystem:
    def __init__(self):
        # Mock database: list of dictionaries
        self.appointments = [
            {
                "customer_name": "Alice Smith",
                "phone_number": "+15550101",
                "appointment_time": datetime.datetime.now() + datetime.timedelta(hours=2),
                "reminded": False
            },
            {
                "customer_name": "Bob Jones",
                "phone_number": "+15550202",
                "appointment_time": datetime.datetime.now() + datetime.timedelta(days=1),
                "reminded": False
            }
        ]

    def send_sms_gateway(self, phone, message):
        """Simulates an API call to an SMS provider like Twilio."""
        print(f"--- SMS SENT TO {phone} ---")
        print(f"Message: {message}")
        print("---------------------------\n")

    def check_and_send_reminders(self, lead_time_hours=24):
        now = datetime.datetime.now()
        reminder_threshold = now + datetime.timedelta(hours=lead_time_hours)

        for appt in self.appointments:
            if not appt["reminded"] and now < appt["appointment_time"] <= reminder_threshold:
                message = (
                    f"Hello {appt['customer_name']}, this is a reminder for your "
                    f"appointment on {appt['appointment_time'].strftime('%Y-%m-%d at %H:%M')}. "
                    f"Please reply 'C' to confirm."
                )
                
                self.send_sms_gateway(appt["phone_number"], message)
                appt["reminded"] = True

    def add_appointment(self, name, phone, dt_string):
        new_appt = {
            "customer_name": name,
            "phone_number": phone,
            "appointment_time": datetime.datetime.strptime(dt_string, "%Y-%m-%d %H:%M"),
            "reminded": False
        }
        self.appointments.append(new_appt)

# --- Execution ---
if __name__ == "__main__":
    scheduler = AppointmentReminderSystem()

    # Add a new appointment for tomorrow
    tomorrow_str = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
    scheduler.add_appointment("Charlie Brown", "+15550303", tomorrow_str)

    print("Checking for appointments requiring reminders (24-hour lead time)...\n")
    scheduler.check_and_send_reminders(lead_time_hours=24)