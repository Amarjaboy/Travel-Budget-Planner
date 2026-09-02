# Travel Budget Planner

A desktop travel budget planner built with Python and Tkinter.

## Features

- Convert your travel budget between currencies using live exchange rates
- Calculate your daily spending limit automatically from your trip dates
- Check public holidays across your entire trip date range
- Track expenses (date, category, description, amount, currency)
- Compare travel costs between two countries
- Get AI-generated travel budget advice (via the Gemini API)
- Extract price values from free-typed text using regular expressions
- Save trips and expenses as JSON and CSV files

## Project structure

- `main.py` — the Tkinter application (UI only; delegates all logic to the classes below)
- `currency_converter.py` — `CurrencyConverter`: currency code validation, conversion, price extraction
- `trip_budget.py` — `TripBudget`: trip validation and daily-limit calculation
- `expense.py` — `Expense`: a single validated expense record
- `budget_report.py` — `BudgetReport`: saving trips/expenses to JSON and CSV
- `holiday_service.py` — `HolidayService`: public holiday lookups across a date range
- `gemini_service.py` — `GeminiService`: AI travel advice via the Gemini API

## Setup

```bash
pip install -r requirements.txt
```

To use the AI Advice tab, set an environment variable before running:

```bash
export GEMINI_API_KEY=your-key-here
```

## Run

```bash
python main.py
```
