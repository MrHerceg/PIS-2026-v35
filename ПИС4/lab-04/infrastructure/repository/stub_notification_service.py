# infrastructure/repository/stub_notification_service.py
from application.ports import NotificationService


class StubNotificationService(NotificationService):
    """Заглушка сервиса уведомлений — выводит сообщения в консоль."""

    def send_trip_created(self, owner_id: str, trip_id: str, title: str) -> None:
        print(
            f"[УВЕДОМЛЕНИЕ] Пользователю {owner_id}: "
            f"поездка '{title}' (id={trip_id[:8]}...) успешно создана!"
        )
