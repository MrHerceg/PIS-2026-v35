# application/command/handlers/create_trip_handler.py
from application.command.create_trip_command import CreateTripCommand
from application.ports import NotificationService, TripRepository
from domain.models.trip import Trip


class CreateTripHandler:
    """
    Обработчик команды CreateTripCommand.

    Шаги:
        1. Валидация данных (выполняется в команде через __post_init__)
        2. Создание доменной модели Trip
        3. Сохранение через репозиторий
        4. Отправка уведомления пользователю
        5. Возврат trip_id
    """

    def __init__(
        self,
        repository: TripRepository,
        notification_service: NotificationService,
    ) -> None:
        self._repo = repository
        self._notifier = notification_service

    def handle(self, command: CreateTripCommand) -> str:
        trip = Trip(
            owner_id=command.owner_id,
            title=command.title,
            start_date=command.start_date,
            end_date=command.end_date,
            budget=command.budget,
        )

        self._repo.save(trip)

        self._notifier.send_trip_created(
            owner_id=command.owner_id,
            trip_id=str(trip.id),
            title=command.title,
        )

        return str(trip.id)
