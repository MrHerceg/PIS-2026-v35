# application/command/handlers/add_note_handler.py
from application.command.add_note_command import AddNoteCommand
from application.ports import TripRepository
from domain.models.trip import Note


class AddNoteHandler:
    def __init__(self, repository: TripRepository) -> None:
        self._repo = repository

    def handle(self, command: AddNoteCommand) -> str:
        trip = self._repo.find_by_id(command.trip_id)
        if trip is None:
            raise ValueError(f"Поездка с id={command.trip_id} не найдена")
        note = Note(text=command.text)
        trip.add_note(note)
        self._repo.save(trip)
        return str(note.id)
