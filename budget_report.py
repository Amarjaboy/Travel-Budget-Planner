import csv
import json


class BudgetReport:
    @staticmethod
    def export_expenses_csv(expenses, filename):
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["date", "category", "description", "amount", "currency"]
            )
            writer.writeheader()
            for expense in expenses:
                writer.writerow(expense.to_dict())

    @staticmethod
    def save_expenses_json(expenses, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([expense.to_dict() for expense in expenses], file, indent=4)

    @staticmethod
    def save_trip_json(trip, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(trip.to_dict(), file, indent=4)
