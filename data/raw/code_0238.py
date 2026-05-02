import time
from plyer import notification

def dispatch_security_alert():
    """
    Simulates a security detection event and triggers an 
    urgent system notification.
    """
    alert_title = "⚠️ URGENT: Security Alert"
    alert_message = (
        "Potential unauthorized access detected on your account. "
        "Please change your password immediately to secure your data."
    )

    notification.notify(
        title=alert_title,
        message=alert_message,
        app_name="SecurityCenter",
        timeout=0,  # 0 often keeps the notification visible until dismissed
        ticker="Security Warning!",
        toast=False
    )

def main():
    print("Security monitoring service is running...")
    
    # Simulate a security trigger event
    time.sleep(3)
    
    print("[ALERT] Security anomaly detected! Dispatching notification...")
    dispatch_security_alert()
    
    print("Action required: User has been prompted for a password change.")

if __name__ == "__main__":
    # Dependency: pip install plyer
    main()