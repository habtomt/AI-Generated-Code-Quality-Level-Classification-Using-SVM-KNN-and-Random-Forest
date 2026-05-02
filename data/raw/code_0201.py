# event_invitation.py
from datetime import datetime, timedelta
from email.message import EmailMessage

class EventManager:
    def __init__(self, event_name, event_date):
        self.event_name = event_name
        self.event_date = event_date
        self.attendees = []

    def send_invites(self, emails):
        for email in emails:
            msg = EmailMessage()
            msg.set_content(f"You're invited to {self.event_name} on {self.event_date}!")
            msg['Subject'] = f"Invitation: {self.event_name}"
            msg['To'] = email
            self.attendees.append({'email': email, 'rsvp_status': 'Pending'})
            print(f"Invite sent to {email}")

    def send_reminders(self):
        reminder_threshold = self.event_date - timedelta(days=1)
        if datetime.now() >= reminder_threshold:
            for attendee in self.attendees:
                if attendee['rsvp_status'] != 'Declined':
                    print(f"Reminder sent to {attendee['email']}")

if __name__ == "__main__":
    event = EventManager("Tech Summit", datetime.now() + timedelta(days=2))
    event.send_invites(["frank@example.com", "grace@example.com"])
    event.send_reminders()