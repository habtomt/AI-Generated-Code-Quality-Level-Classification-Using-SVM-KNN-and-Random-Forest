import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json

class VideoAnalyticsDashboard:
    def __init__(self, db_name="analytics.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Tracking views and core metrics
            cursor.execute('''CREATE TABLE IF NOT EXISTS video_events (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                video_id TEXT,
                                user_id TEXT,
                                event_type TEXT, -- 'view', 'click', 'complete'
                                watch_time_seconds INTEGER,
                                total_duration INTEGER,
                                timestamp DATETIME)''')
            conn.commit()

    def log_event(self, video_id, user_id, event_type, watch_time, total_duration):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO video_events 
                              (video_id, user_id, event_type, watch_time_seconds, total_duration, timestamp)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (video_id, user_id, event_type, watch_time, total_duration, datetime.now()))
            conn.commit()

    def get_retention_data(self, video_id):
        query = f"SELECT watch_time_seconds, total_duration FROM video_events WHERE video_id = '{video_id}'"
        with sqlite3.connect(self.db_name) as conn:
            df = pd.read_sql_query(query, conn)
            
        if df.empty:
            return None
        
        df['retention_rate'] = (df['watch_time_seconds'] / df['total_duration']) * 100
        return df['retention_rate'].mean()

    def generate_report(self, days=7):
        start_date = datetime.now() - timedelta(days=days)
        query = "SELECT * FROM video_events WHERE timestamp >= ?"
        
        with sqlite3.connect(self.db_name) as conn:
            df = pd.read_sql_query(query, conn, params=(start_date,))

        if df.empty:
            print("No data available for the selected period.")
            return

        # Aggregating Metrics
        summary = {
            "total_views": len(df[df['event_type'] == 'view']),
            "unique_viewers": df['user_id'].nunique(),
            "avg_watch_time": df['watch_time_seconds'].mean(),
            "completion_rate": (len(df[df['event_type'] == 'complete']) / len(df)) * 100
        }

        # Visualization
        plt.figure(figsize=(10, 6))
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp').resample('D').size().plot(kind='line', title='Daily Video Views')
        plt.xlabel('Date')
        plt.ylabel('Views')
        plt.grid(True)
        plt.savefig('analytics_report.png')
        
        return json.dumps(summary, indent=4)

if __name__ == "__main__":
    dashboard = VideoAnalyticsDashboard()

    # Mock Data Injection
    dashboard.log_event("vid_101", "user_A", "view", 45, 120)
    dashboard.log_event("vid_101", "user_B", "complete", 120, 120)
    dashboard.log_event("vid_102", "user_C", "view", 10, 300)

    # Generate Custom Report
    print("--- Video Engagement Summary ---")
    report_json = dashboard.generate_report(days=30)
    print(report_json)

    avg_retention = dashboard.get_retention_data("vid_101")
    print(f"\nAverage Retention for vid_101: {avg_retention:.2f}%")