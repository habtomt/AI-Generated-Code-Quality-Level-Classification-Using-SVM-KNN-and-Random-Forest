"""
Auto-generated Python code
Scenario : Cloud Database Services
Prompt   : response_004.txt
Run      : 3
"""

# Import required libraries
import psutil
import time
import os
import subprocess
import json
import requests

# Define constants
HOSTNAME = 'YOUR_HOSTNAME'
DATABASE_HOST = 'YOUR_DATABASE_HOST'
DATABASE_PORT = 5432
DATABASE_USER = 'YOUR_DATABASE_USER'
DATABASE_PASSWORD = 'YOUR_DATABASE_PASSWORD'
DATABASE_NAME = 'YOUR_DATABASE_NAME'

# Set up Prometheus and Grafana
PROMETHEUS_HOST = 'http://localhost:9090'
GRAFANA_HOST = 'http://localhost:3000'

# Define monitoring functions
def get_cpu_usage():
    """Get current CPU usage"""
    return psutil.cpu_percent()

def get_memory_usage():
    """Get current memory usage"""
    return psutil.virtual_memory().percent

def get_query_performance():
    """Get query performance (assuming PostgreSQL)"""
    try:
        # Use 'pg_stat_statements' extension to get query performance
        query = f"""
            SELECT 
                query, 
                calls, 
                total_time, 
                avg_time, 
                rows
            FROM 
                pg_stat_statements
            ORDER BY 
                total_time DESC
            LIMIT 10;
        """
        result = subprocess.check_output(['psql', '-h', DATABASE_HOST, '-p', str(DATABASE_PORT), '-U', DATABASE_USER, DATABASE_PASSWORD, '-c', query]).decode('utf-8')
        return json.loads(result)
    except Exception as e:
        print(f"Error getting query performance: {e}")

def get_storage_usage():
    """Get current storage usage (assuming PostgreSQL)"""
    try:
        # Use 'pg_stat_user_tables' to get storage usage
        query = f"""
            SELECT 
                tablespace_name, 
                sum(table_rows) AS rows, 
                sum(table_size) AS size
            FROM 
                pg_stat_user_tables
            GROUP BY 
                tablespace_name;
        """
        result = subprocess.check_output(['psql', '-h', DATABASE_HOST, '-p', str(DATABASE_PORT), '-U', DATABASE_USER, DATABASE_PASSWORD, '-c', query]).decode('utf-8')
        return json.loads(result)
    except Exception as e:
        print(f"Error getting storage usage: {e}")

# Define alert conditions
def check_cpu_usage(cpu_usage):
    """Check if CPU usage exceeds 80%"""
    return cpu_usage > 80

def check_memory_usage(memory_usage):
    """Check if memory usage exceeds 80%"""
    return memory_usage > 80

def check_query_performance(query_performance):
    """Check if query performance is slow (e.g., > 100ms)"""
    return any(query['avg_time'] > 100 for query in query_performance['rows'])

def check_storage_usage(storage_usage):
    """Check if storage usage exceeds 80%"""
    return any(size['size'] > 0.8 * total_size for size, total_size in storage_usage['rows'])

# Define optimization suggestions
def suggest_cpu_optimization(cpu_usage):
    """Suggest CPU optimization (e.g., add more nodes or upgrade instance)"""
    return f"CPU usage is high ({cpu_usage}%). Consider adding more nodes or upgrading instance."

def suggest_memory_optimization(memory_usage):
    """Suggest memory optimization (e.g., add more RAM or upgrade instance)"""
    return f"Memory usage is high ({memory_usage}%). Consider adding more RAM or upgrading instance."

def suggest_query_optimization(query_performance):
    """Suggest query optimization (e.g., reindex tables or update statistics)"""
    return f"Query performance is slow. Consider reindexing tables or updating statistics."

def suggest_storage_optimization(storage_usage):
    """Suggest storage optimization (e.g., add more storage or upgrade instance)"""
    return f"Storage usage is high. Consider adding more storage or upgrading instance."

# Monitor and alert
while True:
    try:
        # Get current metrics
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        query_performance = get_query_performance()
        storage_usage = get_storage_usage()

        # Check alert conditions
        if check_cpu_usage(cpu_usage):
            print(f"CPU usage alert: {suggest_cpu_optimization(cpu_usage)}")
        if check_memory_usage(memory_usage):
            print(f"Memory usage alert: {suggest_memory_optimization(memory_usage)}")
        if check_query_performance(query_performance):
            print(f"Query performance alert: {suggest_query_optimization(query_performance)}")
        if check_storage_usage(storage_usage):
            print(f"Storage usage alert: {suggest_storage_optimization(storage_usage)}")

        # Push metrics to Prometheus
        metrics = {
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'query_performance': query_performance,
            'storage_usage': storage_usage,
        }
        response = requests.post(f"{PROMETHEUS_HOST}/api/v1/write", json=metrics)

        # Push notifications to Grafana
        notify_url = f"{GRAFANA_HOST}/api/plugins/grafana-alerts/v1/notify"
        notification = {
            'title': f"Monitoring Alert: {HOSTNAME}",
            'message': f"CPU usage: {cpu_usage}%, Memory usage: {memory_usage}%, Query performance: {query_performance}, Storage usage: {storage_usage}",
        }
        response = requests.post(notify_url, json=notification)

        # Sleep for 1 minute before next check
        time.sleep(60)
    except Exception as e:
        print(f"Error monitoring: {e}")