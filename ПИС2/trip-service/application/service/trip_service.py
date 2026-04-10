from domain.exceptions.domain_exceptions import DateConflictError

class TripService:
    """Реализация use-cases управления поездками"""

    def __init__(self, repository, geo_service, notification_service):
        self.repository           = repository
        self.geo_service          = geo_service
        self.notification_service = notification_service

    def create(self, command):
        """Логика создания поездки"""
        # 1. Создать доменную модель Trip
        # 2. Валидировать даты (end > start)
        # 3. Сохранить через repository
        # 4. Отправить уведомление
        raise NotImplementedError("Реализация будет в Lab #4")

    def get_by_id(self, trip_id: str):
        """Получение поездки по ID"""
        raise NotImplementedError("Реализация будет в Lab #4")
