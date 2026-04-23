from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.trip import Trip


class GetTripUseCase(ABC):
    """Incoming port: defines the contract for retrieving trips."""

    @abstractmethod
    def get_trip_by_id(self, trip_id: str) -> Optional[Trip]:
        """
        Retrieves a single trip by its UUID.

        Returns:
            Trip if found, None otherwise.
        """
        ...

    @abstractmethod
    def get_all_trips(self) -> List[Trip]:
        """
        Retrieves all existing trips.

        Returns:
            List of Trip objects.
        """
        ...
