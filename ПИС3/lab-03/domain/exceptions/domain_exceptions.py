class DomainException(Exception):
    """Базовое исключение доменного уровня."""
    pass


class TripAlreadyCompletedException(DomainException):
    def __init__(self, trip_id=None):
        msg = "Trip is already completed"
        if trip_id:
            msg += f" (id={trip_id})"
        super().__init__(msg)


class InvalidRouteException(DomainException):
    pass


class InvalidNoteException(DomainException):
    pass
