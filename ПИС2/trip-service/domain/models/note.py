from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Note:
    content: str
    created_at: datetime = field(default_factory=datetime.now)
    id: UUID = field(default_factory=uuid4)

    def __repr__(self) -> str:
        return f"Note(id={self.id}, created_at={self.created_at}, content='{self.content[:30]}...')"
