class TripController:
    """Упрощённый контроллер для обработки HTTP-запросов"""

    def __init__(self, trip_service):
        self.service = trip_service

    def create_trip(self, owner_id: str, title: str,
                    start_date: str, end_date: str, budget: float):
        """Эндпоинт для создания поездки"""
        # В ЛР №4 здесь будет вызов команды CreateTripCommand
        print(f"[API] Получен запрос на создание поездки от {owner_id}")
        # return self.service.create(...)
