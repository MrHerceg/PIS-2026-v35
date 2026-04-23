from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class TripView:
    """Read Model: проекция поездки для быстрого чтения"""
    id:          str
    owner_id:    str
    title:       str
    start_date:  date
    end_date:    date
    budget:      float
    status:      str
    place_count: int      = 0   # денормализованное поле
    note_count:  int      = 0   # денормализованное поле
    created_at:  datetime = field(default_factory=datetime.now)
