from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DateRange:
    start_date: date
    end_date: date

    def __post_init__(self):
        # Поддержка строк формата "YYYY-MM-DD"
        if isinstance(self.start_date, str):
            object.__setattr__(self, 'start_date', date.fromisoformat(self.start_date))
        if isinstance(self.end_date, str):
            object.__setattr__(self, 'end_date', date.fromisoformat(self.end_date))

        if self.start_date > self.end_date:
            raise ValueError(
                f"Start date ({self.start_date}) cannot be later than end date ({self.end_date})"
            )

    @property
    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days

    def __str__(self):
        return f"{self.start_date} — {self.end_date} ({self.duration_days} days)"
