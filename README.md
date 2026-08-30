# Travel Budget Planner - Python Advanced Project

A complete Tkinter-based travel budget application demonstrating:

- Object-Oriented Programming (OOP)
- Regular expressions
- Exception handling
- File handling with CSV and JSON
- REST API requests
- Currency conversion
- Public-holiday checking
- Expense tracking
- Country cost comparison
- Optional Gemini AI travel-budget advice

## Project files

- `main.py` - graphical user interface
- `currency_converter.py` - exchange-rate API and currency validation
- `trip_budget.py` - trip and daily-budget calculations
- `expense.py` - Expense OOP class and validation
- `budget_report.py` - CSV/JSON file handling
- `api_services.py` - Nager.Date and Gemini API services
- `requirements.txt` - Python dependency list

## Requirements

Python 3.12 is recommended.

Install the dependency:

```bash
pip install -r requirements.txt
```

Tkinter normally comes with Python on Windows.

## Run

```bash
python main.py
```

## Gemini AI setup

The AI feature is optional.

Create an environment variable named:

`GEMINI_API_KEY`

You can also set:

`GEMINI_MODEL`

If `GEMINI_MODEL` is not set, the program uses `gemini-2.5-flash`.

Do not put your API key directly inside the Python source code.

## APIs

The program uses:
- Open Exchange Rates-style public endpoint from ExchangeRate-API/open.er-api.com for currency rates.
- Nager.Date for public holidays.
- Google Gemini REST API for optional AI advice.

Internet access is required for live currency rates, holidays, and Gemini advice.

## Notes

For the country comparison screen, enter both daily costs in the same currency before comparing them. The application deliberately does not pretend that daily costs in different currencies can be compared directly.

The application catches common input, network, JSON, and API errors so that the GUI does not simply crash when a service is unavailable.
