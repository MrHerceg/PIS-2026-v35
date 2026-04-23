from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


@dataclass
class CreateTripCommand:
    title: str
    start_date: date
    end_date: date
    budget: float
    description: str = ""


class CreateTripUseCase(ABC):
    """Incoming port: defines the contract for creating a new trip."""

    @abstractmethod
    def create_trip(self, command: CreateTripCommand) -> str:
        """
        Creates a new trip based on the given command.

        Returns:
            str: The UUID of the newly created trip.
        """
        ...
