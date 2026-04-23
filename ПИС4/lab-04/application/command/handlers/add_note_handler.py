# application/command/handlers/add_note_handler.py
from application.command.add_note_command import AddNoteCommand
from application.ports import TripRepository
from domain.models.trip import Note


class AddNoteHandler:
    """
    Обработчик команды AddNoteCommand.

    Шаги:
        1. Загрузка поездки из репозитория
        2. Проверка существования поездки
        3. Создание объекта Note
        4. Добавление заметки через trip.add_note()
        5. Сохранение изменений
    """

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
