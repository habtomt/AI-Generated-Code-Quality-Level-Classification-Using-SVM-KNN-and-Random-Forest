import json
from kafka import KafkaConsumer, KafkaProducer

# Configuration for the open-source platform (Apache Kafka)
KAFKA_BROKER = 'localhost:9092'
INPUT_TOPIC = 'raw-data-feed'
OUTPUT_TOPIC = 'processed-data'

def transform_data(data):
    """
    Applies business logic transformations to the incoming stream.
    """
    # Example transformation: cleaning strings and calculating a derived value
    if 'value' in data:
        data['processed_value'] = data['value'] * 1.15
        data['status'] = 'TRANSFORMED'
        data['source'] = 'real-time-engine'
    return data

def run_event_processor():
    # Initialize Consumer to listen to the data feed
    consumer = KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='latest',
        group_id='event-processor-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # Initialize Producer to output transformed data
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    print(f"Listening for events on topic: {INPUT_TOPIC}...")

    try:
        for message in consumer:
            raw_event = message.value
            
            # Real-time transformation
            processed_event = transform_data(raw_event)
            
            # Forwarding to the next stage in the pipeline
            producer.send(OUTPUT_TOPIC, value=processed_event)
            producer.flush()
            
            print(f"Processed event ID: {raw_event.get('id', 'unknown')}")

    except KeyboardInterrupt:
        print("Stopping processor...")
    finally:
        consumer.close()
        producer.close()

if __name__ == "__main__":
    run_event_processor()