# place-service/app/events.py
import json
import os
from typing import Any, Dict

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
EXCHANGE = "poekhali.events"


def publish_event(event_type: str, payload: Dict[str, Any]) -> None:
    """Публикует событие в RabbitMQ exchange."""
    try:
        import pika
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
        body = json.dumps({"event": event_type, **payload}, default=str)
        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=event_type,
            body=body.encode(),
            properties=pika.BasicProperties(delivery_mode=2, content_type="application/json"),
        )
        connection.close()
        print(f"[EventBus] Published: {event_type}")
    except Exception as exc:
        print(f"[EventBus] Failed to publish {event_type}: {exc}")
