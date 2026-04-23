from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid


@dataclass
class DomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: datetime = field(default_factory=datetime.now)
