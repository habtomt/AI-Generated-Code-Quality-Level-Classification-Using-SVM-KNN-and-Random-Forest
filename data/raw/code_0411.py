"""
Auto-generated Python code
Scenario : Data Storage
Prompt   : response_004.txt
Run      : 3
"""

# Import required libraries
import paho.mqtt.client as mqtt
import json
import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        TimedRotatingFileHandler('iot_data.log', when='midnight', interval=1, encoding='utf-8', backupCount=30),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Define the MQTT broker connection settings
MQTT_BROKER = 'YOUR_MQTT_BROKER_URL'
MQTT_PORT = 1883
MQTT_TOPIC = 'YOUR_IOT_DEVICE_TOPIC'

# Define the IoT device credentials
DEVICE_ID = 'YOUR_DEVICE_ID'
DEVICE_TOKEN = 'YOUR_DEVICE_TOKEN'

# Set up the MQTT client
client = mqtt.Client()

try:
    # Establish the MQTT connection
    client.connect(MQTT_BROKER, MQTT_PORT)
    logger.info('Connected to MQTT broker')

    # Define a callback function for incoming MQTT messages
    def on_message(client, userdata, message):
        try:
            # Parse the incoming message as JSON
            data = json.loads(message.payload.decode('utf-8'))
            logger.info(f'Received data from IoT device {data["device_id"]}: {data["data"]}')

            # Save the data to a file for later analysis
            with open('iot_data.json', 'a') as f:
                json.dump(data, f)
                f.write('\n')
        except json.JSONDecodeError as e:
            logger.error(f'Failed to parse incoming message: {e}')

    # Subscribe to the IoT device topic
    client.subscribe(MQTT_TOPIC)
    logger.info(f'Subscribed to topic {MQTT_TOPIC}')

    # Define a callback function for incoming MQTT messages
    client.on_message = on_message

    # Start the MQTT message loop
    client.loop_forever()

except Exception as e:
    logger.error(f'Failed to establish MQTT connection: {e}')

finally:
    # Disconnect from the MQTT broker
    client.disconnect()
    logger.info('Disconnected from MQTT broker')