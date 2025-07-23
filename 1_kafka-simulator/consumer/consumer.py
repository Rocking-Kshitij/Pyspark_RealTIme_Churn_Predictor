from kafka import KafkaConsumer
import json

# Kafka Config
# BROKER = "localhost:9092"
BROKER = "54.160.8.148:9092" # for ec2
TOPIC = "customer_events"


# Initialize Kafka consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)


if __name__ == "__main__":
    print("Waiting for messages......")
    for message in consumer:
        data = message.value
        print(f"Received: {data}", flush = True)