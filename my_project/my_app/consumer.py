import os
import sys
import django
from confluent_kafka import Consumer
import json

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')

# Setup Django
django.setup()

from my_app.models import UserData

# Initialize Kafka consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['userData'])

def save_to_db(data):
    user_data = json.loads(data)
    UserData.objects.create(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password']
    )

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        print(f"Received message: {msg.value().decode('utf-8')}")
        save_to_db(msg.value().decode('utf-8'))
finally:
    consumer.close()
