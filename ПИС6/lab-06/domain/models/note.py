from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Note:
    """Заметка, прикреплённая к поездке."""

    note_id: str
    trip_id: str
    text: str
    created_at: datetime = field(default_factory=datetime.now)

    def __repr__(self) -> str:
        return f"Note(id={self.note_id!r}, trip={self.trip_id!r})"
