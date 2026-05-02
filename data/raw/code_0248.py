import datetime

class SupportTicketSMSSystem:
    def __init__(self):
        # Mock database of support tickets
        self.tickets = {
            "TKT-101": {
                "customer_name": "James Holden",
                "phone": "+14155550198",
                "status": "Open",
                "history": []
            },
            "TKT-202": {
                "customer_name": "Naomi Nagata",
                "phone": "+14155550254",
                "status": "In Progress",
                "history": []
            }
        }

    def _trigger_sms_gateway(self, phone, content):
        """Simulates the low-level API call to an SMS service."""
        print(f"--- OUTGOING SMS ---")
        print(f"Recipient: {phone}")
        print(f"Body: {content}")
        print(f"Timestamp: {datetime.datetime.now().strftime('%H:%M:%S')}")
        print("---------------------\n")

    def update_ticket_status(self, ticket_id, new_status, internal_note=""):
        if ticket_id not in self.tickets:
            print(f"Error: Ticket {ticket_id} not found.")
            return

        ticket = self.tickets[ticket_id]
        old_status = ticket["status"]
        ticket["status"] = new_status
        ticket["history"].append({
            "timestamp": datetime.datetime.now(),
            "from": old_status,
            "to": new_status,
            "note": internal_note
        })

        # Construct and send the notification
        message = (
            f"Hi {ticket['customer_name']}, your support inquiry ({ticket_id}) "
            f"has been updated to: {new_status.upper()}. "
        )
        
        if new_status.lower() == "resolved":
            message += "Thank you for your patience. You can reply HELP for more assistance."
        else:
            message += "We will notify you of further updates."

        self._trigger_sms_gateway(ticket["phone"], message)

    def notify_custom_update(self, ticket_id, update_text):
        if ticket_id in self.tickets:
            ticket = self.tickets[ticket_id]
            message = f"Update for {ticket_id}: {update_text}"
            self._trigger_sms_gateway(ticket["phone"], message)

# --- Execution Simulation ---
if __name__ == "__main__":
    support_system = SupportTicketSMSSystem()

    # Scenario 1: Status update to In Progress
    support_system.update_ticket_status(
        "TKT-101", 
        "In Progress", 
        "Engineer assigned to investigate connectivity issue."
    )

    # Scenario 2: Sending a manual specific update
    support_system.notify_custom_update(
        "TKT-202", 
        "Our technician is currently reviewing your account logs."
    )

    # Scenario 3: Resolving the ticket
    support_system.update_ticket_status(
        "TKT-101", 
        "Resolved", 
        "Hardware reset completed remotely."
    )