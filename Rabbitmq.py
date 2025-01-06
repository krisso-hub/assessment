
import os
import time
import requests
from prometheus_client import start_http_server, Gauge

# Environment variables for RabbitMQ details
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "password")

# Prometheus metrics
rabbitmq_queue_messages = Gauge(
    "rabbitmq_individual_queue_messages",
    "Total count of messages in RabbitMQ queue",
    ["host", "vhost", "name"]
)
rabbitmq_queue_messages_ready = Gauge(
    "rabbitmq_individual_queue_messages_ready",
    "Count of ready messages in RabbitMQ queue",
    ["host", "vhost", "name"]
)
rabbitmq_queue_messages_unacknowledged = Gauge(
    "rabbitmq_individual_queue_messages_unacknowledged",
    "Count of unacknowledged messages in RabbitMQ queue",
    ["host", "vhost", "name"]
)

def fetch_rabbitmq_queues():
    """Fetch queue information from RabbitMQ HTTP API"""
    url = f"http://{RABBITMQ_HOST}:15672/api/queues"
    try:
        response = requests.get(url, auth=(RABBITMQ_USER, RABBITMQ_PASSWORD))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching RabbitMQ data: {e}")
        return []

def update_metrics():
    """Update Prometheus metrics with RabbitMQ queue data"""
    queues = fetch_rabbitmq_queues()
    for queue in queues:
        host = RABBITMQ_HOST
        vhost = queue.get("vhost", "")
        name = queue.get("name", "")
        messages = queue.get("messages", 0)
        messages_ready = queue.get("messages_ready", 0)
        messages_unacknowledged = queue.get("messages_unacknowledged", 0)

        rabbitmq_queue_messages.labels(host=host, vhost=vhost, name=name).set(messages)
        rabbitmq_queue_messages_ready.labels(host=host, vhost=vhost, name=name).set(messages_ready)
        rabbitmq_queue_messages_unacknowledged.labels(host=host, vhost=vhost, name=name).set(messages_unacknowledged)

if __name__ == "__main__":
    # Start Prometheus HTTP server
    start_http_server(8000)
    print("Prometheus RabbitMQ exporter started on port 8000")

    # Periodically fetch and update metrics
    while True:
        update_metrics()
        time.sleep(15)  # Poll every 15 seco