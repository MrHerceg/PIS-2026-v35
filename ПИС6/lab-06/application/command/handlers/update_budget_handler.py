from application.command.update_budget_command import UpdateBudgetCommand


class UpdateBudgetHandler:
    def __init__(self, repository):
        self._repo = repository

    def handle(self, command: UpdateBudgetCommand) -> None:
        trip = self._repo.find_by_id(command.trip_id)
        if trip is None:
            raise ValueError(f"Trip '{command.trip_id}' not found")
        trip.budget = command.budget
        self._repo.save(trip)
