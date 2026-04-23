# infrastructure/adapter/out/notification_service.py
from application.ports import EventPublisher, NotificationService


class EventNotificationService(NotificationService):
    """
    Адаптер уведомлений: публикует событие trip.created через EventPublisher.
    """

    def __init__(self, publisher: EventPublisher) -> None:
        self._publisher = publisher

    def send_trip_created(self, owner_id: str, trip_id: str, title: str) -> None:
        self._publisher.publish(
            event_type="trip.created",
            payload={
                "owner_id": owner_id,
                "trip_id": trip_id,
                "title": title,
            },
        )
