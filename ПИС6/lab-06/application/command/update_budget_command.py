from dataclasses import dataclass


@dataclass
class UpdateBudgetCommand:
    trip_id: str
    budget: float
