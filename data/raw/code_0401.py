"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_004.txt
Run      : 1
"""

# Import necessary libraries
import kafka
from kafka import KafkaProducer, KafkaConsumer
import json
import logging
from influxdb import InfluxDBClient
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)

# Kafka setup
KAFKA_BOOTSTRAP_SERVER = 'localhost:9092'
KAFKA_TOPIC = 'iot-data'
KAFKA_PROCESSED_TOPIC = 'processed-iot-data'

# InfluxDB setup
INFLUXDB_HOST = 'localhost'
INFLUXDB_PORT = 8086
INFLUXDB_DB = 'iot_data'
INFLUXDB_USER = 'your_username'
INFLUXDB_PASSWORD = 'your_password'

# IoT device data ingestion
def ingest_data(temperature, humidity):
    """
    Send data to Kafka topic.
    """
    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER)
    data = {'temperature': temperature, 'humidity': humidity}
    producer.send(KAFKA_TOPIC, json.dumps(data).encode('utf-8'))
    producer.flush()

# Real-time processing
def process_data():
    """
    Consume data from Kafka topic, process it, and send to another topic.
    """
    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
                             auto_offset_reset='earliest',
                             enable_auto_commit=True)
    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER)

    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        processed_data = {'temperature': data['temperature'], 'humidity': data['humidity']}
        logging.info(f"Received data: {processed_data}")
        
        # Example processing: convert temperature to Celsius
        if 'temperature' in processed_data:
            processed_data['temperature'] = (processed_data['temperature'] - 32) * 5.0/9.0
        
        producer.send(KAFKA_PROCESSED_TOPIC, json.dumps(processed_data).encode('utf-8'))

# Storage in InfluxDB
def store_data(temperature, humidity):
    """
    Store data in InfluxDB.
    """
    client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT, username=INFLUXDB_USER, password=INFLUXDB_PASSWORD)
    client.switch_database(INFLUXDB_DB)
    
    data = [
        {
            "measurement": "iot_sensor_data",
            "fields": {
                "temperature": temperature,
                "humidity": humidity
            },
            "time": datetime.now().isoformat(),
            "tags": {
                "device": "iot_device"
            }
        }
    ]
    
    client.write_points(data)

# Main function
def main():
    try:
        # Ingest data from IoT device
        ingest_data(22.5, 60)
        
        # Process data in real-time
        process_data()
        
        # Store data in InfluxDB
        store_data(22.5, 60)
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()