# application/command/handlers/add_place_handler.py
import warnings

from application.command.add_place_command import AddPlaceToRouteCommand
from application.ports import GeoService, TripRepository


class AddPlaceToRouteHandler:
    """
    Обработчик команды AddPlaceToRouteCommand.

    Шаги:
        1. Загрузка поездки из репозитория
        2. Проверка существования поездки
        3. Получение данных о месте через GeoService
        4. Проверка бюджета (предупреждение при превышении)
        5. Добавление места через метод trip.add_place()
        6. Сохранение изменений
    """

    COST_PER_PLACE = 50.0  # условная стоимость добавления места, BYN

    def __init__(self, repository: TripRepository, geo_service: GeoService) -> None:
        self._repo = repository
        self._geo = geo_service

    def handle(self, command: AddPlaceToRouteCommand) -> None:
        trip = self._repo.find_by_id(command.trip_id)
        if trip is None:
            raise ValueError(f"Поездка с id={command.trip_id} не найдена")

        place = self._geo.find_place(command.place_id)
        if place is None:
            raise ValueError(f"Место с id={command.place_id} не найдено")

        projected_spend = len(trip.route) * self.COST_PER_PLACE + self.COST_PER_PLACE
        if projected_spend > trip.budget:
            warnings.warn(
                f"Добавление места '{place.name}' может превысить бюджет "
                f"(бюджет: {trip.budget}, ожидаемые расходы: {projected_spend})",
                UserWarning,
                stacklevel=2,
            )

        trip.add_place(place)
        self._repo.save(trip)
