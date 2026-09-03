from dataclasses import dataclass
from datetime import datetime
import re

"""
Defines the Expense data class and handles field validation and dict conversion.
"""
@dataclass
class Expense:
    date: str
    category: str
    description: str
    amount: float
    currency: str

    def __post_init__(self):
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Expense date must use YYYY-MM-DD format.") from exc

        if not self.category:
            raise ValueError("Expense category is required.")

        if self.amount <= 0:
            raise ValueError("Expense amount must be greater than zero.")

        self.currency = self.currency.strip().upper()
        if not re.fullmatch(r"[A-Z]{3}", self.currency):
            raise ValueError("Currency must be a 3-letter code such as NGN or USD.")

    def to_dict(self):
        return {
            "date": self.date,
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
            "currency": self.currency,
        }
