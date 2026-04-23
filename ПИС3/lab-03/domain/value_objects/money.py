from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError(f"Amount cannot be negative: {self.amount}")
        if not self.currency or len(self.currency) != 3 or not self.currency.isalpha():
            raise ValueError(
                f"Currency must be a 3-letter code (e.g. USD, EUR, BYN): '{self.currency}'"
            )
        object.__setattr__(self, 'currency', self.currency.upper())

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract {other.currency} from {self.currency}")
        if self.amount < other.amount:
            raise ValueError("Result would be negative")
        return Money(self.amount - other.amount, self.currency)

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"
