from datetime import datetime


class TripBudgetError(Exception):
    """Raised when trip information is invalid."""


class TripBudget:
    def __init__(self, home_currency, destination_currency, amount, start_date, end_date):
        self.home_currency = home_currency.upper()
        self.destination_currency = destination_currency.upper()

        if amount <= 0:
            raise TripBudgetError("Budget amount must be greater than zero.")

        try:
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            self.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise TripBudgetError("Dates must use YYYY-MM-DD format.") from exc

        if self.end_date < self.start_date:
            raise TripBudgetError("End date cannot be before start date.")

        self.amount = float(amount)
        self.duration_days = (self.end_date - self.start_date).days + 1

    def daily_limit(self, converted_budget):
        if self.duration_days <= 0:
            raise TripBudgetError("Trip duration must be positive.")
        return converted_budget / self.duration_days

    def to_dict(self):
        return {
            "home_currency": self.home_currency,
            "destination_currency": self.destination_currency,
            "amount": self.amount,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "duration_days": self.duration_days,
        }
