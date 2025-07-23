from kafka import KafkaProducer
import json
import time, random
from datetime import datetime

# Kafka Config
#BROKER = "localhost:9092"
BROKER = "54.160.8.148:9092" # for ec2
TOPIC = "customer_events"
print("started", flush = True)
time.sleep(2)
# Initialize producer
producer = KafkaProducer(
    bootstrap_servers=BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Event types
events = ['visit', 'add_to_cart', 'purchase', 'feedback']

def generate_event():
    return {
        "customer_id": random.randint(1000, 1050),
        "event": random.choice(events),
        "timestamp": datetime.utcnow().isoformat(),
        "product_id": f"P{random.randint(100, 999)}",
        "amount": round(random.uniform(100, 2000), 2)
    }

if __name__ == "__main__":
    print("Starting Kafka Producer...")
    while True:
        event = generate_event()
        print("Sending:", event, flush = True)
        producer.send(TOPIC, value=event)
        print(f"Sent: {event}", flush = True)
        time.sleep(random.randint(1, 10)*0.01)  # Send a message every 30 second
