# infrastructure/adapter/out/rabbitmq_event_publisher.py
"""
Адаптер для публикации событий через RabbitMQ (pika).
"""
import json
import os

from application.ports import EventPublisher

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE_NAME = "poekhali.events"


class RabbitMQEventPublisher(EventPublisher):
    """
    Исходящий адаптер: публикует события в RabbitMQ exchange.
    Соединение создаётся лениво при первой публикации.
    """

    def __init__(self) -> None:
        self._connection = None
        self._channel = None

    def _ensure_connected(self) -> None:
        try:
            import pika
            if self._connection is None or self._connection.is_closed:
                params = pika.URLParameters(RABBITMQ_URL)
                self._connection = pika.BlockingConnection(params)
                self._channel = self._connection.channel()
                self._channel.exchange_declare(
                    exchange=EXCHANGE_NAME,
                    exchange_type="topic",
                    durable=True,
                )
        except Exception as exc:
            print(f"[RabbitMQ] Не удалось подключиться: {exc}")
            self._channel = None

    def publish(self, event_type: str, payload: dict) -> None:
        self._ensure_connected()
        if self._channel is None:
            print(f"[RabbitMQ] Публикация пропущена (нет соединения): {event_type}")
            return
        try:
            import pika
            body = json.dumps({"event": event_type, **payload}, default=str)
            self._channel.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key=event_type,
                body=body.encode(),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # persistent
                    content_type="application/json",
                ),
            )
            print(f"[RabbitMQ] Опубликовано событие: {event_type}")
        except Exception as exc:
            print(f"[RabbitMQ] Ошибка публикации: {exc}")

    def close(self) -> None:
        if self._connection and not self._connection.is_closed:
            self._connection.close()
