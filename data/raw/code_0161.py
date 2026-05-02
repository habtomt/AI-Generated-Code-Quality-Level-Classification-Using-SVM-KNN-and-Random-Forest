import time
import mysql.connector

# Database connection details
db_config = {
    'user': 'monitor_user',
    'password': 'password',
    'host': 'db_host',
    'database': 'db_name'
}

def collect_metrics():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Example: Monitoring Query Performance (Slow queries)
        cursor.execute("SHOW GLOBAL STATUS LIKE 'Threads_connected';")
        threads = cursor.fetchone()
        
        print(f"[{time.ctime()}] Active Connections: {threads[1]}")
        
        # Check for anomaly
        if int(threads[1]) > 100:
            print("ALERT: High connection count anomaly detected!")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Monitoring error: {e}")

if __name__ == "__main__":
    while True:
        collect_metrics()
        time.sleep(60)