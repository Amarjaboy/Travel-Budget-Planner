import json
import csv


class BudgetReport:
    # This is the class for the budget report

    @staticmethod
    def save_trip_json(trip, filename="trip.json"):
        data = {
            "home_currency": trip.home_currency,
            "destination_currency": trip.destination_currency,
            "amount": trip.amount,
            "start_date": trip.start_date.isoformat(),
            "end_date": trip.end_date.isoformat(),
            "duration_days": trip.duration_days,
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def save_expenses_json(expenses, filename="expenses.json"):
        data = []

        for expense in expenses:
            if hasattr(expense, "to_dict"):
                data.append(expense.to_dict())
            else:
                data.append({
                    "category": expense.category,
                    "amount": expense.amount
                })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def export_expenses_csv(expenses, filename="expenses.csv"):
        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Date",
                "Category",
                "Description",
                "Amount",
                "Currency"
            ])

            for expense in expenses:
                if hasattr(expense, "date"):
                    writer.writerow([
                        expense.date,
                        expense.category,
                        expense.description,
                        expense.amount,
                        expense.currency
                    ])