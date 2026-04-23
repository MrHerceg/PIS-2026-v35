# application/command/add_note_command.py
from dataclasses import dataclass


@dataclass
class AddNoteCommand:
    """
    Команда для добавления заметки к поездке.

    Поля:
        trip_id — идентификатор поездки (обязательное)
        text    — текст заметки (обязательное, не пустой)
    """
    trip_id: str
    text: str

    def __post_init__(self) -> None:
        if not self.trip_id:
            raise ValueError("trip_id обязательно")
        if not self.text or not self.text.strip():
            raise ValueError("text обязателен и не должен быть пустым")
