import datetime
import random

class OrderTrackingSMSService:
    def __init__(self):
        # Simulated database of orders
        self.orders = {
            "ORD-7712": {
                "customer": "Elena Gilbert",
                "phone": "+13105550123",
                "item": "Vintage Leather Journal",
                "status": "Processing"
            },
            "ORD-9945": {
                "customer": "Stefan Salvatore",
                "phone": "+13105550456",
                "item": "Silver Pocket Watch",
                "status": "Shipped"
            }
        }

    def _send_sms_payload(self, phone, text):
        """Simulates the SMS API request."""
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] SMS to {phone}:")
        print(f"  > {text}\n")

    def update_order_status(self, order_id, new_status, tracking_number=None):
        if order_id not in self.orders:
            print(f"Order {order_id} not found.")
            return

        order = self.orders[order_id]
        order["status"] = new_status
        
        # Message construction logic
        message = f"Hi {order['customer']}, your order {order_id} for '{order['item']}' is now: {new_status.upper()}."
        
        if new_status.lower() == "shipped" and tracking_number:
            message += f" Track here: https://shipit.com/t/{tracking_number}"
        elif new_status.lower() == "out for delivery":
            message += " Our driver should arrive by 8 PM tonight."
        elif new_status.lower() == "delivered":
            message += " It was left near your front door. Enjoy!"

        self._send_sms_payload(order["phone"], message)

    def trigger_mock_shipment(self, order_id):
        tracking_ref = f"TRK{random.randint(100000, 999999)}"
        self.update_order_status(order_id, "Shipped", tracking_ref)

# --- Simulation ---
if __name__ == "__main__":
    service = OrderTrackingSMSService()

    # Update order to Shipped
    service.trigger_mock_shipment("ORD-7712")

    # Update order to Out for Delivery
    service.update_order_status("ORD-9945", "Out for Delivery")

    # Update order to Delivered
    service.update_order_status("ORD-7712", "Delivered")