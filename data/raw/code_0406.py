"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_004.txt
Run      : 2
"""

# Import necessary libraries
import pandas as pd
import json
import paho.mqtt.client as mqtt
import time
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# IoT Device Data Collector Class
class IotDeviceDataCollector:
    def __init__(self, broker_url, client_id, api_key):
        self.broker_url = broker_url
        self.client_id = client_id
        self.api_key = api_key  # Replace with YOUR_API_KEY
        self.mqtt_client = mqtt.Client(client_id)
        self.mqtt_client.username_pw_set(api_key)
        self.storage = []

    def connect_to_broker(self):
        try:
            logging.info('Connecting to MQTT broker...')
            self.mqtt_client.connect(self.broker_url)
        except Exception as e:
            logging.error(f'Failed to connect to MQTT broker: {str(e)}')
            return False
        return True

    def subscribe_to_topics(self, topics):
        try:
            logging.info('Subscribing to topics...')
            self.mqtt_client.subscribe(topics)
        except Exception as e:
            logging.error(f'Failed to subscribe to topics: {str(e)}')
            return False
        return True

    def start_data_collection(self, topic):
        try:
            logging.info('Starting data collection...')
            self.mqtt_client.on_message = self.on_message
            self.mqtt_client.loop_start()
            self.mqtt_client.subscribe(topic)
        except Exception as e:
            logging.error(f'Failed to start data collection: {str(e)}')
            return False
        return True

    def on_message(self, client, userdata, message):
        try:
            logging.info('Received message: {}'.format(message.payload.decode('utf-8')))
            data = json.loads(message.payload)
            self.storage.append(data)
        except Exception as e:
            logging.error(f'Failed to process message: {str(e)}')

    def stop_data_collection(self):
        try:
            logging.info('Stopping data collection...')
            self.mqtt_client.loop_stop()
        except Exception as e:
            logging.error(f'Failed to stop data collection: {str(e)}')
            return False
        return True

    def process_and_store_data(self):
        try:
            logging.info('Processing and storing data...')
            self.storage = pd.DataFrame(self.storage)
            self.storage.to_csv('iot_device_data.csv', index=False)
        except Exception as e:
            logging.error(f'Failed to process and store data: {str(e)}')
            return False
        return True

# Usage example
if __name__ == '__main__':
    # Replace with your MQTT broker URL and API key
    broker_url = 'localhost'
    client_id = 'iot_device_data_collector'
    api_key = 'YOUR_API_KEY'

    collector = IotDeviceDataCollector(broker_url, client_id, api_key)
    if collector.connect_to_broker() and collector.subscribe_to_topics('iot/device/data'):
        topic = 'iot/device/data'
        if collector.start_data_collection(topic):
            time.sleep(60)  # Collect data for 1 minute
            collector.stop_data_collection()
            if collector.process_and_store_data():
                logging.info('Data stored successfully')
            else:
                logging.error('Failed to store data')
        else:
            logging.error('Failed to start data collection')
    else:
        logging.error('Failed to connect to MQTT broker or subscribe to topic')