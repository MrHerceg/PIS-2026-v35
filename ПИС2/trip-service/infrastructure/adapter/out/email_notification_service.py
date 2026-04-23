from application.port.out.notification_service import NotificationService
from domain.models.trip import Trip


class EmailNotificationService(NotificationService):
    """
    Outgoing adapter: simulates sending email notifications.
    In production, replace with SMTP / SendGrid / etc.
    """

    def notify_trip_created(self, trip: Trip, recipient_email: str) -> None:
        print(
            f"[EMAIL] To: {recipient_email}\n"
            f"Subject: Поездка '{trip.title}' создана!\n"
            f"Тело: Ваша поездка с {trip.start_date} по {trip.end_date} "
            f"с бюджетом {trip.budget} BYN успешно создана.\n"
        )

    def notify_trip_reminder(self, trip: Trip, recipient_email: str) -> None:
        print(
            f"[EMAIL] To: {recipient_email}\n"
            f"Subject: Напоминание: поездка '{trip.title}' скоро!\n"
            f"Тело: Не забудьте — поездка начинается {trip.start_date}.\n"
        )
