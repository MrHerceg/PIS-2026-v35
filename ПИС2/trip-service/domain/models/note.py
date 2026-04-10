from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Note:
    """Value Object: Заметка к поездке"""
    text:       str
    created_at: datetime = datetime.now()
