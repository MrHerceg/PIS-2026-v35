import uuid
from datetime import datetime
from domain.exceptions.domain_exceptions import InvalidNoteException


class Note:
    def __init__(self, text: str):
        if not text or not text.strip():
            raise InvalidNoteException("Note text cannot be empty")
        self.id: str = str(uuid.uuid4())
        self.text: str = text.strip()
        self.created_at: datetime = datetime.now()

    def __repr__(self):
        return f"Note(id={self.id!r}, text={self.text!r})"
