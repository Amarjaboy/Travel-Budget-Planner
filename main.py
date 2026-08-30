import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import csv
import os
import re
from datetime import datetime


# ============================================================
# API ERROR
# ============================================================

class APIError(Exception):
    """Used when an API request fails."""


# ============================================================
# COUNTRY LIST
# ============================================================

COUNTRIES = {
    "Nigeria": "NG",
    "Ghana": "GH",
    "United Kingdom": "GB",
    "United States": "US",
    "Qatar": "QA",
    "United Arab Emirates": "AE",
    "Saudi Arabia": "SA",
    "Canada": "CA",
    "Germany": "DE",
    "France": "FR",
    "Italy": "IT",
    "Spain": "ES",
    "Portugal": "PT",
    "Netherlands": "NL",
    "Belgium": "BE",
    "Switzerland": "CH",
    "Austria": "AT",
    "Australia": "AU",
    "New Zealand": "NZ",
    "South Africa": "ZA",
    "Kenya": "KE",
    "Egypt": "EG",
    "Morocco": "MA",
    "Turkey": "TR",
    "India": "IN",
    "China": "CN",
    "Japan": "JP",
    "South Korea": "KR",
    "Singapore": "SG",
    "Malaysia": "MY",
    "Thailand": "TH",
    "Indonesia": "ID",
    "Russia": "RU",
    "Brazil": "BR",
    "Mexico": "MX",
    "Argentina": "AR",
    "United States Minor Outlying Islands": "UM",
    "Ireland": "IE",
    "Norway": "NO",
    "Sweden": "SE",
    "Denmark": "DK",
    "Finland": "FI",
    "Poland": "PL",
    "Czech Republic": "CZ",
    "Hungary": "HU",
    "Greece": "GR",
    "Romania": "RO",
    "Ukraine": "UA",
    "Israel": "IL",
    "Pakistan": "PK",
    "Bangladesh": "BD",
    "Sri Lanka": "LK",
    "Nepal": "NP",
    "Philippines": "PH",
    "Vietnam": "VN",
    "Cambodia": "KH",
    "Iceland": "IS",
    "Luxembourg": "LU",
    "Malta": "MT",
    "Cyprus": "CY",
    "Croatia": "HR",
    "Serbia": "RS",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Bulgaria": "BG",
    "Estonia": "EE",
    "Latvia": "LV",
    "Lithuania": "LT",
    "Iceland": "IS",
    "Colombia": "CO",
    "Chile": "CL",
    "Peru": "PE",
    "Uruguay": "UY",
    "Ecuador": "EC",
    "Costa Rica": "CR",
    "Panama": "PA",
    "Jamaica": "JM",
    "Bahamas": "BS",
    "Barbados": "BB",
    "Trinidad and Tobago": "TT",
    "Tanzania": "TZ",
    "Uganda": "UG",
    "Rwanda": "RW",
    "Ethiopia": "ET",
    "Gambia": "GM",
    "Senegal": "SN",
    "Sierra Leone": "SL",
    "Liberia": "LR",
    "Cameroon": "CM",
    "Benin": "BJ",
    "Togo": "TG",
    "Niger": "NE",
    "Chad": "TD",
    "Mali": "ML",
    "Burkina Faso": "BF",
    "Cote d'Ivoire": "CI",
    "Zimbabwe": "ZW",
    "Zambia": "ZM",
    "Botswana": "BW",
    "Namibia": "NA",
    "Mozambique": "MZ",
    "Mauritius": "MU",
    "Seychelles": "SC",
    "Algeria": "DZ",
    "Tunisia": "TN",
    "Libya": "LY",
    "Sudan": "SD",
    "Jordan": "JO",
    "Lebanon": "LB",
    "Kuwait": "KW",
    "Bahrain": "BH",
    "Oman": "OM",
    "Iraq": "IQ",
    "Iran": "IR",
}


# ============================================================
# WORLD CURRENCY LIST
# ============================================================

CURRENCIES = [
    "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD",
    "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF",
    "BMD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BYN",
    "BZD", "CAD", "CDF", "CHF", "CLP", "CNY", "COP", "CRC",
    "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP",
    "ERN", "ETB", "EUR", "FJD", "FKP", "FOK", "GBP", "GEL",
    "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD",
    "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "IMP", "INR",
    "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES",
    "KGS", "KHR", "KID", "KMF", "KRW", "KWD", "KYD", "KZT",
    "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL",
    "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR",
    "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK",
    "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR",
    "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR",
    "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL",
    "SOS", "SRD", "SSP", "STN", "SYP", "SZL", "THB", "TJS",
    "TMT", "TND", "TOP", "TRY", "TTD", "TVD", "TWD", "TZS",
    "UAH", "UGX", "USD", "UYU", "UZS", "VES", "VND", "VUV",
    "WST", "XAF", "XCD", "XOF", "XPF", "YER", "ZAR", "ZMW",
    "ZWL"
]


# ============================================================
# HOLIDAY SERVICE
# ============================================================

class HolidayService:

    BASE_URL = (
        "https://date.nager.at/api/v3/PublicHolidays/"
        "{year}/{country_code}"
    )

    def get_holidays(self, year, country_code):

        country_code = country_code.strip().upper()

        if len(country_code) != 2:
            raise APIError("Country code must contain 2 letters.")

        try:
            response = requests.get(
                self.BASE_URL.format(
                    year=year,
                    country_code=country_code
                ),
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, list):
                raise APIError("Unexpected holiday data.")

            return data

        except requests.RequestException as error:
            raise APIError(
                f"Could not connect to public holiday service:\n{error}"
            )

        except ValueError:
            raise APIError(
                "The public holiday service returned invalid data."
            )

    def check_date(self, travel_date, country_code):

        holidays = self.get_holidays(
            travel_date.year,
            country_code
        )

        for holiday in holidays:

            if holiday.get("date") == travel_date.strftime("%Y-%m-%d"):

                return {
                    "is_holiday": True,
                    "name": (
                        holiday.get("localName")
                        or holiday.get("name")
                        or "Public Holiday"
                    )
                }

        return {
            "is_holiday": False,
            "name": ""
        }


# ============================================================
# CURRENCY SERVICE
# ============================================================

class CurrencyService:

    BASE_URL = "https://open.er-api.com/v6/latest/{currency}"

    def get_rate(self, from_currency, to_currency):

        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()

        if from_currency == to_currency:
            return 1.0

        try:

            response = requests.get(
                self.BASE_URL.format(currency=from_currency),
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            rates = data.get("rates", {})

            if to_currency not in rates:
                raise APIError(
                    f"Currency {to_currency} is not supported."
                )

            return float(rates[to_currency])

        except requests.RequestException as error:

            raise APIError(
                f"Currency API request failed:\n{error}"
            )

        except (ValueError, TypeError):

            raise APIError(
                "Currency API returned invalid data."
            )

    def convert(self, amount, from_currency, to_currency):

        rate = self.get_rate(
            from_currency,
            to_currency
        )

        return amount * rate


# ============================================================
# GEMINI AI SERVICE
# ============================================================

class GeminiService:

    API_URL = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/{model}:generateContent"
    )

    def __init__(self):

        self.api_key = os.getenv(
            "GEMINI_API_KEY",
            ""
        ).strip()

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.7-flash"
        ).strip()

    def generate_advice(self, prompt):

        if not self.api_key:

            raise APIError(
                "GEMINI_API_KEY is not configured.\n\n"
                "Set your Gemini API key and try again."
            )

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "You are a professional travel budgeting "
                                "assistant.\n"
                                "Give practical and realistic travel "
                                "budget advice.\n"
                                "Use clear headings and bullet points.\n"
                                "Do not invent exact prices.\n\n"
                                + prompt
                            )
                        }
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

        try:

            response = requests.post(
                self.API_URL.format(
                    model=self.model
                ),
                headers=headers,
                json=payload,
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            candidates = data.get(
                "candidates",
                []
            )

            if not candidates:
                raise APIError(
                    "Gemini returned no response."
                )

            parts = candidates[0].get(
                "content",
                {}
            ).get(
                "parts",
                []
            )

            text = ""

            for part in parts:

                if "text" in part:

                    text += part["text"]

            if not text:

                raise APIError(
                    "Gemini returned no usable advice."
                )

            return text

        except requests.RequestException as error:

            raise APIError(
                f"Gemini request failed:\n{error}"
            )

        except ValueError:

            raise APIError(
                "Gemini returned invalid JSON."
            )


# ============================================================
# MAIN APPLICATION
# ============================================================

class TravelBudgetApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "✈ Travel Budget Planner"
        )

        self.root.geometry(
            "1200x760"
        )

        self.root.minsize(
            1000,
            650
        )

        # ----------------------------------------------------
        # COLORS
        # ----------------------------------------------------

        self.GREEN = "#075E3A"
        self.DARK_GREEN = "#043D27"
        self.LIGHT_GREEN = "#E8F5EF"
        self.GOLD = "#D4AF37"
        self.WHITE = "#FFFFFF"
        self.BG = "#F4F7F5"
        self.TEXT = "#263238"
        self.GRAY = "#6B7280"
        self.RED = "#B42318"
        self.ORANGE = "#B54708"

        self.root.configure(
            bg=self.BG
        )

        # ----------------------------------------------------
        # SERVICES
        # ----------------------------------------------------

        self.holiday_service = HolidayService()
        self.currency_service = CurrencyService()
        self.gemini_service = GeminiService()

        # ----------------------------------------------------
        # VARIABLES
        # ----------------------------------------------------

        self.destination_country = tk.StringVar()
        self.destination_code = tk.StringVar()

        self.home_currency = tk.StringVar(
            value="NGN"
        )

        self.destination_currency = tk.StringVar(
            value="USD"
        )

        self.amount = tk.StringVar()

        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()

        self.budget = tk.StringVar()
        self.duration = tk.StringVar()

        self.total_expense = 0.0
        self.expenses = []

        # ----------------------------------------------------
        # STYLE
        # ----------------------------------------------------

        self.setup_styles()

        # ----------------------------------------------------
        # BUILD GUI
        # ----------------------------------------------------

        self.create_header()
        self.create_notebook()

        self.create_trip_tab()
        self.create_expense_tab()
        self.create_compare_tab()
        self.create_ai_tab()

        self.show_welcome()


    # ========================================================
    # STYLES
    # ========================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TNotebook",
            background=self.BG,
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            padding=(25, 12),
            font=("Segoe UI", 10, "bold"),
            background="#E5E7EB"
        )

        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", self.GREEN)
            ],
            foreground=[
                ("selected", self.WHITE)
            ]
        )

        style.configure(
            "TLabel",
            background=self.BG,
            foreground=self.TEXT,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Title.TLabel",
            background=self.GREEN,
            foreground=self.WHITE,
            font=("Segoe UI", 25, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background=self.GREEN,
            foreground="#D8EDE3",
            font=("Segoe UI", 11)
        )

        style.configure(
            "Section.TLabel",
            background=self.WHITE,
            foreground=self.GREEN,
            font=("Segoe UI", 14, "bold")
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 9)
        )

        style.configure(
            "Green.TButton",
            background=self.GREEN,
            foreground=self.WHITE,
            font=("Segoe UI", 10, "bold"),
            padding=(15, 9)
        )

        style.map(
            "Green.TButton",
            background=[
                ("active", self.DARK_GREEN)
            ]
        )

        style.configure(
            "Gold.TButton",
            background=self.GOLD,
            foreground="#222222",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 9)
        )

        style.map(
            "Gold.TButton",
            background=[
                ("active", "#B89625")
            ]
        )

        style.configure(
            "TEntry",
            padding=8
        )

        style.configure(
            "TCombobox",
            padding=7
        )


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.GREEN,
            height=125
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        title = ttk.Label(
            header,
            text="✈  TRAVEL BUDGET PLANNER",
            style="Title.TLabel"
        )

        title.pack(
            pady=(20, 2)
        )

        subtitle = ttk.Label(
            header,
            text="Plan Smart  •  Track Expenses  •  Travel Better",
            style="Subtitle.TLabel"
        )

        subtitle.pack()


    # ========================================================
    # NOTEBOOK
    # ========================================================

    def create_notebook(self):

        self.notebook = ttk.Notebook(
            self.root
        )

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=15
        )


    # ========================================================
    # CARD
    # ========================================================

    def create_card(self, parent):

        card = tk.Frame(
            parent,
            bg=self.WHITE,
            bd=1,
            relief="solid"
        )

        return card


    # ========================================================
    # TRIP TAB
    # ========================================================

    def create_trip_tab(self):

        self.trip_tab = tk.Frame(
            self.notebook,
            bg=self.BG
        )

        self.notebook.add(
            self.trip_tab,
            text="  Trip Budget  "
        )

        card = self.create_card(
            self.trip_tab
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        title = ttk.Label(
            card,
            text="Trip Details",
            style="Section.TLabel"
        )

        title.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            padx=20,
            pady=(18, 15)
        )

        # Destination

        ttk.Label(
            card,
            text="Destination country:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=8
        )

        self.country_combo = ttk.Combobox(
            card,
            textvariable=self.destination_country,
            values=sorted(COUNTRIES.keys()),
            state="readonly",
            width=30
        )

        self.country_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=10
        )

        self.country_combo.bind(
            "<<ComboboxSelected>>",
            self.country_selected
        )

        ttk.Label(
            card,
            text="Country code:"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=20
        )

        self.code_entry = ttk.Entry(
            card,
            textvariable=self.destination_code,
            width=15
        )

        self.code_entry.grid(
            row=1,
            column=3,
            padx=10
        )

        # Home currency

        ttk.Label(
            card,
            text="Home currency:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=8
        )

        self.home_combo = ttk.Combobox(
            card,
            textvariable=self.home_currency,
            values=CURRENCIES,
            state="readonly",
            width=30
        )

        self.home_combo.grid(
            row=2,
            column=1,
            padx=10
        )

        # Destination currency

        ttk.Label(
            card,
            text="Destination currency:"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=20
        )

        self.dest_currency_combo = ttk.Combobox(
            card,
            textvariable=self.destination_currency,
            values=CURRENCIES,
            state="readonly",
            width=15
        )

        self.dest_currency_combo.grid(
            row=2,
            column=3,
            padx=10
        )

        # Budget

        ttk.Label(
            card,
            text="Travel budget:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=8
        )

        self.budget_entry = ttk.Entry(
            card,
            textvariable=self.budget,
            width=32
        )

        self.budget_entry.grid(
            row=3,
            column=1,
            padx=10
        )

        # Duration

        ttk.Label(
            card,
            text="Duration (days):"
        ).grid(
            row=3,
            column=2,
            sticky="w",
            padx=20
        )

        self.duration_entry = ttk.Entry(
            card,
            textvariable=self.duration,
            width=17
        )

        self.duration_entry.grid(
            row=3,
            column=3,
            padx=10
        )

        # Dates

        ttk.Label(
            card,
            text="Travel start date:"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=20,
            pady=8
        )

        ttk.Entry(
            card,
            textvariable=self.start_date,
            width=32
        ).grid(
            row=4,
            column=1,
            padx=10
        )

        ttk.Label(
            card,
            text="Travel end date:"
        ).grid(
            row=4,
            column=2,
            sticky="w",
            padx=20
        )

        ttk.Entry(
            card,
            textvariable=self.end_date,
            width=17
        ).grid(
            row=4,
            column=3,
            padx=10
        )

        # Buttons

        button_frame = tk.Frame(
            card,
            bg=self.WHITE
        )

        button_frame.grid(
            row=5,
            column=0,
            columnspan=4,
            sticky="w",
            padx=20,
            pady=20
        )

        ttk.Button(
            button_frame,
            text="Calculate Budget",
            style="Green.TButton",
            command=self.calculate_budget
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ttk.Button(
            button_frame,
            text="Check Public Holidays",
            style="Gold.TButton",
            command=self.check_holidays
        ).pack(
            side="left",
            padx=10
        )

        ttk.Button(
            button_frame,
            text="Save Trip JSON",
            command=self.save_trip
        ).pack(
            side="left",
            padx=10
        )

        # Results

        result_card = self.create_card(
            self.trip_tab
        )

        result_card.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        ttk.Label(
            result_card,
            text="Results",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.result_text = tk.Text(
            result_card,
            height=12,
            bg="#FBFDFC",
            fg=self.TEXT,
            font=("Consolas", 11),
            relief="flat",
            padx=15,
            pady=15
        )

        self.result_text.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.result_text.config(
            state="disabled"
        )


    # ========================================================
    # COUNTRY SELECTED
    # ========================================================

    def country_selected(self, event=None):

        country = self.destination_country.get()

        code = COUNTRIES.get(
            country,
            ""
        )

        self.destination_code.set(
            code
        )


    # ========================================================
    # EXPENSE TAB
    # ========================================================

    def create_expense_tab(self):

        self.expense_tab = tk.Frame(
            self.notebook,
            bg=self.BG
        )

        self.notebook.add(
            self.expense_tab,
            text="  Expenses  "
        )

        card = self.create_card(
            self.expense_tab
        )

        card.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        ttk.Label(
            card,
            text="Track Your Expenses",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            padx=20,
            pady=20
        )

        form = tk.Frame(
            card,
            bg=self.WHITE
        )

        form.pack(
            fill="x",
            padx=20
        )

        ttk.Label(
            form,
            text="Category:"
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.expense_category = ttk.Entry(
            form,
            width=25
        )

        self.expense_category.grid(
            row=0,
            column=1,
            padx=10
        )

        ttk.Label(
            form,
            text="Amount:"
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.expense_amount = ttk.Entry(
            form,
            width=20
        )

        self.expense_amount.grid(
            row=0,
            column=3,
            padx=10
        )

        ttk.Button(
            form,
            text="Add Expense",
            style="Green.TButton",
            command=self.add_expense
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        # Expense table

        table_frame = tk.Frame(
            card,
            bg=self.WHITE
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        columns = (
            "category",
            "amount"
        )

        self.expense_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        self.expense_tree.heading(
            "category",
            text="Category"
        )

        self.expense_tree.heading(
            "amount",
            text="Amount"
        )

        self.expense_tree.column(
            "category",
            width=250
        )

        self.expense_tree.column(
            "amount",
            width=200
        )

        self.expense_tree.pack(
            fill="both",
            expand=True
        )

        button_frame = tk.Frame(
            card,
            bg=self.WHITE
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_expense
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Clear Expenses",
            command=self.clear_expenses
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Save Expenses",
            style="Green.TButton",
            command=self.save_expenses
        ).pack(
            side="left",
            padx=5
        )

        self.expense_total_label = ttk.Label(
            button_frame,
            text="Total: 0.00",
            font=("Segoe UI", 12, "bold")
        )

        self.expense_total_label.pack(
            side="right",
            padx=10
        )


    # ========================================================
    # ADD EXPENSE
    # ========================================================

    def add_expense(self):

        category = self.expense_category.get().strip()

        amount_text = self.expense_amount.get().strip()

        if not category:

            messagebox.showwarning(
                "Missing Category",
                "Please enter an expense category."
            )

            return

        try:

            amount = float(
                amount_text
            )

            if amount < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid expense amount."
            )

            return

        self.expenses.append(
            {
                "category": category,
                "amount": amount
            }
        )

        self.expense_tree.insert(
            "",
            "end",
            values=(
                category,
                f"{amount:,.2f}"
            )
        )

        self.total_expense += amount

        self.expense_total_label.config(
            text=f"Total: {self.total_expense:,.2f}"
        )

        self.expense_category.delete(
            0,
            "end"
        )

        self.expense_amount.delete(
            0,
            "end"
        )


    # ========================================================
    # DELETE EXPENSE
    # ========================================================

    def delete_expense(self):

        selected = self.expense_tree.selection()

        if not selected:
            return

        for item in selected:

            values = self.expense_tree.item(
                item,
                "values"
            )

            amount = float(
                str(values[1]).replace(",", "")
            )

            self.total_expense -= amount

            self.expense_tree.delete(
                item
            )

            self.expenses = [
                expense
                for expense in self.expenses
                if not (
                    expense["category"] == values[0]
                    and abs(
                        expense["amount"] - amount
                    ) < 0.001
                )
            ]

        self.expense_total_label.config(
            text=f"Total: {self.total_expense:,.2f}"
        )


    # ========================================================
    # CLEAR EXPENSES
    # ========================================================

    def clear_expenses(self):

        self.expenses.clear()

        self.total_expense = 0.0

        for item in self.expense_tree.get_children():

            self.expense_tree.delete(
                item
            )

        self.expense_total_label.config(
            text="Total: 0.00"
        )


    # ========================================================
    # SAVE EXPENSES
    # ========================================================

    def save_expenses(self):

        if not self.expenses:

            messagebox.showwarning(
                "No Expenses",
                "There are no expenses to save."
            )

            return

        try:

            with open(
                "expenses.json",
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.expenses,
                    file,
                    indent=4
                )

            with open(
                "expenses.csv",
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(
                    file
                )

                writer.writerow(
                    ["Category", "Amount"]
                )

                for expense in self.expenses:

                    writer.writerow(
                        [
                            expense["category"],
                            expense["amount"]
                        ]
                    )

            messagebox.showinfo(
                "Saved",
                "Expenses saved successfully.\n\n"
                "expenses.json\n"
                "expenses.csv"
            )

        except OSError as error:

            messagebox.showerror(
                "Save Error",
                str(error)
            )


    # ========================================================
    # CALCULATE BUDGET
    # ========================================================

    def calculate_budget(self):

        try:

            budget = float(
                self.budget.get()
            )

            duration = int(
                self.duration.get()
            )

            if budget <= 0 or duration <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Enter a valid positive budget and duration."
            )

            return

        daily_limit = budget / duration

        remaining = (
            budget -
            self.total_expense
        )

        destination = (
            self.destination_country.get()
            or "Not selected"
        )

        currency = (
            self.home_currency.get()
            or "NGN"
        )

        result = (
            "✈ TRAVEL BUDGET SUMMARY\n"
            "══════════════════════════════\n\n"
            f"Destination: {destination}\n"
            f"Budget: {budget:,.2f} {currency}\n"
            f"Duration: {duration} days\n"
            f"Daily limit: {daily_limit:,.2f} {currency}\n\n"
            "EXPENSES\n"
            "──────────────────────────────\n"
            f"Total expenses: "
            f"{self.total_expense:,.2f} {currency}\n"
            f"Remaining budget: "
            f"{remaining:,.2f} {currency}\n"
        )

        if remaining < 0:

            result += (
                "\n⚠ WARNING:\n"
                "Your expenses are above your budget."
            )

        else:

            result += (
                "\n✓ STATUS:\n"
                "Your current expenses are within budget."
            )

        self.set_result(
            result
        )

        self.save_complete_report(
            budget,
            duration,
            daily_limit,
            remaining
        )


    # ========================================================
    # PUBLIC HOLIDAY
    # ========================================================

    def check_holidays(self):

        date_text = self.start_date.get().strip()

        country_code = (
            self.destination_code.get()
            .strip()
            .upper()
        )

        if not date_text:

            messagebox.showwarning(
                "Missing Date",
                "Enter the travel start date."
            )

            return

        try:

            travel_date = datetime.strptime(
                date_text,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            messagebox.showerror(
                "Invalid Date",
                "Use YYYY-MM-DD."
            )

            return

        if len(country_code) != 2:

            messagebox.showerror(
                "Country Code",
                "Country code must contain 2 letters."
            )

            return

        try:

            result = self.holiday_service.check_date(
                travel_date,
                country_code
            )

            if result["is_holiday"]:

                self.set_result(
                    "⚠ PUBLIC HOLIDAY WARNING\n"
                    "══════════════════════════════\n\n"
                    f"Date: {date_text}\n"
                    f"Holiday: {result['name']}\n\n"
                    "⚠ This date is a public holiday.\n"
                    "You should consider choosing another "
                    "travel date."
                )

                messagebox.showwarning(
                    "Public Holiday",
                    f"{result['name']}\n\n"
                    "This date is a public holiday."
                )

            else:

                self.set_result(
                    "✓ TRAVEL DATE AVAILABLE\n"
                    "══════════════════════════════\n\n"
                    f"Date: {date_text}\n\n"
                    "No public holiday was found for "
                    "this date."
                )

                messagebox.showinfo(
                    "Travel Date Available",
                    "No public holiday was found."
                )

        except APIError as error:

            messagebox.showwarning(
                "Holiday Service",
                f"{error}\n\n"
                "The program can continue, but the "
                "holiday status could not be confirmed."
            )


    # ========================================================
    # SAVE TRIP
    # ========================================================

    def save_trip(self):

        data = {
            "destination_country":
                self.destination_country.get(),

            "country_code":
                self.destination_code.get(),

            "home_currency":
                self.home_currency.get(),

            "destination_currency":
                self.destination_currency.get(),

            "budget":
                self.budget.get(),

            "duration":
                self.duration.get(),

            "start_date":
                self.start_date.get(),

            "end_date":
                self.end_date.get(),

            "expenses":
                self.expenses
        }

        try:

            with open(
                "trip.json",
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

            messagebox.showinfo(
                "Saved",
                "Trip saved successfully as trip.json."
            )

        except OSError as error:

            messagebox.showerror(
                "Save Error",
                str(error)
            )


    # ========================================================
    # COMPLETE REPORT
    # ========================================================

    def save_complete_report(
        self,
        budget,
        duration,
        daily_limit,
        remaining
    ):

        report = {
            "destination":
                self.destination_country.get(),

            "country_code":
                self.destination_code.get(),

            "budget":
                budget,

            "currency":
                self.home_currency.get(),

            "duration":
                duration,

            "daily_limit":
                daily_limit,

            "expenses":
                self.expenses,

            "total_expenses":
                self.total_expense,

            "remaining_budget":
                remaining
        }

        try:

            with open(
                "travel_report.json",
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    report,
                    file,
                    indent=4
                )

            with open(
                "travel_report.csv",
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(
                    file
                )

                writer.writerow(
                    ["Travel Budget Report"]
                )

                writer.writerow(
                    ["Destination", report["destination"]]
                )

                writer.writerow(
                    ["Country Code", report["country_code"]]
                )

                writer.writerow(
                    ["Budget", budget]
                )

                writer.writerow(
                    ["Currency", report["currency"]]
                )

                writer.writerow(
                    ["Duration", duration]
                )

                writer.writerow(
                    ["Daily Limit", daily_limit]
                )

                writer.writerow(
                    ["Total Expenses", self.total_expense]
                )

                writer.writerow(
                    ["Remaining Budget", remaining]
                )

                writer.writerow([])

                writer.writerow(
                    ["Category", "Amount"]
                )

                for expense in self.expenses:

                    writer.writerow(
                        [
                            expense["category"],
                            expense["amount"]
                        ]
                    )

        except OSError:
            pass


    # ========================================================
    # CURRENCY CONVERTER
    # ========================================================

    def create_currency_section(self, parent):

        card = self.create_card(
            parent
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            card,
            text="Currency Converter",
            style="Section.TLabel"
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            padx=20,
            pady=18
        )

        ttk.Label(
            card,
            text="From:"
        ).grid(
            row=1,
            column=0,
            padx=20
        )

        from_combo = ttk.Combobox(
            card,
            values=CURRENCIES,
            state="readonly",
            width=15
        )

        from_combo.set(
            "NGN"
        )

        from_combo.grid(
            row=1,
            column=1,
            padx=10
        )

        ttk.Label(
            card,
            text="To:"
        ).grid(
            row=1,
            column=2
        )

        to_combo = ttk.Combobox(
            card,
            values=CURRENCIES,
            state="readonly",
            width=15
        )

        to_combo.set(
            "USD"
        )

        to_combo.grid(
            row=1,
            column=3,
            padx=10
        )

        ttk.Label(
            card,
            text="Amount:"
        ).grid(
            row=2,
            column=0,
            padx=20,
            pady=15
        )

        amount_entry = ttk.Entry(
            card,
            width=18
        )

        amount_entry.grid(
            row=2,
            column=1
        )

        result_label = ttk.Label(
            card,
            text="Result will appear here.",
            font=("Segoe UI", 11, "bold")
        )

        result_label.grid(
            row=2,
            column=2,
            columnspan=2,
            padx=20
        )

        def convert():

            try:

                amount = float(
                    amount_entry.get()
                )

                result = self.currency_service.convert(
                    amount,
                    from_combo.get(),
                    to_combo.get()
                )

                result_label.config(
                    text=(
                        f"{amount:,.2f} "
                        f"{from_combo.get()} = "
                        f"{result:,.2f} "
                        f"{to_combo.get()}"
                    ),
                    foreground=self.GREEN
                )

            except (ValueError, APIError) as error:

                result_label.config(
                    text=str(error),
                    foreground=self.RED
                )

        ttk.Button(
            card,
            text="Convert",
            style="Green.TButton",
            command=convert
        ).grid(
            row=3,
            column=0,
            columnspan=4,
            pady=15
        )


    # ========================================================
    # PRICE EXTRACTION
    # ========================================================

    def create_price_section(self, parent):

        card = self.create_card(
            parent
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            card,
            text="Price Extractor",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            padx=20,
            pady=15
        )

        ttk.Label(
            card,
            text=(
                "Example: Hotel ₦80,000, Food ₦30,000"
            )
        ).pack(
            anchor="w",
            padx=20
        )

        entry = ttk.Entry(
            card
        )

        entry.pack(
            fill="x",
            padx=20,
            pady=10
        )

        result = ttk.Label(
            card,
            text="Extracted prices: []"
        )

        result.pack(
            anchor="w",
            padx=20,
            pady=5
        )

        def extract():

            text = entry.get()

            numbers = re.findall(
                r"\d[\d,]*",
                text
            )

            prices = []

            for number in numbers:

                number = number.replace(
                    ",",
                    ""
                )

                try:
                    prices.append(
                        float(number)
                    )
                except ValueError:
                    pass

            result.config(
                text=f"Extracted prices: {prices}"
            )

        ttk.Button(
            card,
            text="Extract Prices",
            command=extract
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )


    # ========================================================
    # COMPARE TAB
    # ========================================================

    def create_compare_tab(self):

        self.compare_tab = tk.Frame(
            self.notebook,
            bg=self.BG
        )

        self.notebook.add(
            self.compare_tab,
            text="  Compare Countries  "
        )

        card = self.create_card(
            self.compare_tab
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            card,
            text="Compare Travel Costs",
            style="Section.TLabel"
        ).grid(
            row=0,
            column=0,
            columnspan=6,
            sticky="w",
            padx=20,
            pady=20
        )

        ttk.Label(
            card,
            text="Home currency:"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=8
        )

        self.compare_home = ttk.Combobox(
            card,
            values=CURRENCIES,
            state="readonly",
            width=15
        )

        self.compare_home.set(
            "NGN"
        )

        self.compare_home.grid(
            row=1,
            column=1
        )

        # Country 1

        ttk.Label(
            card,
            text="Country 1:"
        ).grid(
            row=2,
            column=0,
            padx=10
        )

        self.compare_country1 = ttk.Combobox(
            card,
            values=sorted(COUNTRIES.keys()),
            state="readonly",
            width=22
        )

        self.compare_country1.grid(
            row=2,
            column=1
        )

        ttk.Label(
            card,
            text="Currency:"
        ).grid(
            row=2,
            column=2
        )

        self.compare_currency1 = ttk.Combobox(
            card,
            values=CURRENCIES,
            state="readonly",
            width=12
        )

        self.compare_currency1.grid(
            row=2,
            column=3
        )

        ttk.Label(
            card,
            text="Budget:"
        ).grid(
            row=2,
            column=4
        )

        self.compare_budget1 = ttk.Entry(
            card,
            width=15
        )

        self.compare_budget1.grid(
            row=2,
            column=5
        )

        ttk.Label(
            card,
            text="Duration:"
        ).grid(
            row=3,
            column=4
        )

        self.compare_duration1 = ttk.Entry(
            card,
            width=15
        )

        self.compare_duration1.grid(
            row=3,
            column=5
        )

        # Country 2

        ttk.Label(
            card,
            text="Country 2:"
        ).grid(
            row=4,
            column=0,
            padx=10,
            pady=15
        )

        self.compare_country2 = ttk.Combobox(
            card,
            values=sorted(COUNTRIES.keys()),
            state="readonly",
            width=22
        )

        self.compare_country2.grid(
            row=4,
            column=1
        )

        ttk.Label(
            card,
            text="Currency:"
        ).grid(
            row=4,
            column=2
        )

        self.compare_currency2 = ttk.Combobox(
            card,
            values=CURRENCIES,
            state="readonly",
            width=12
        )

        self.compare_currency2.grid(
            row=4,
            column=3
        )

        ttk.Label(
            card,
            text="Budget:"
        ).grid(
            row=4,
            column=4
        )

        self.compare_budget2 = ttk.Entry(
            card,
            width=15
        )

        self.compare_budget2.grid(
            row=4,
            column=5
        )

        ttk.Label(
            card,
            text="Duration:"
        ).grid(
            row=5,
            column=4
        )

        self.compare_duration2 = ttk.Entry(
            card,
            width=15
        )

        self.compare_duration2.grid(
            row=5,
            column=5
        )

        ttk.Button(
            card,
            text="Compare Countries",
            style="Green.TButton",
            command=self.compare_countries
        ).grid(
            row=6,
            column=0,
            columnspan=6,
            pady=20
        )

        result_card = self.create_card(
            self.compare_tab
        )

        result_card.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.compare_result = tk.Text(
            result_card,
            bg="#FBFDFC",
            fg=self.TEXT,
            font=("Consolas", 11),
            relief="flat",
            padx=15,
            pady=15
        )

        self.compare_result.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )


    # ========================================================
    # COMPARE COUNTRIES
    # ========================================================

    def compare_countries(self):

        try:

            home = self.compare_home.get()

            currency1 = self.compare_currency1.get()

            currency2 = self.compare_currency2.get()

            budget1 = float(
                self.compare_budget1.get()
            )

            budget2 = float(
                self.compare_budget2.get()
            )

            duration1 = int(
                self.compare_duration1.get()
            )

            duration2 = int(
                self.compare_duration2.get()
            )

            if duration1 <= 0 or duration2 <= 0:
                raise ValueError

            converted1 = self.currency_service.convert(
                budget1,
                currency1,
                home
            )

            converted2 = self.currency_service.convert(
                budget2,
                currency2,
                home
            )

            daily1 = budget1 / duration1

            daily2 = budget2 / duration2

            country1 = (
                self.compare_country1.get()
                or "Country 1"
            )

            country2 = (
                self.compare_country2.get()
                or "Country 2"
            )

            if converted1 < converted2:

                cheaper = country1

            elif converted2 < converted1:

                cheaper = country2

            else:

                cheaper = "Both countries cost the same."

            result = (
                "🌍 TRAVEL COMPARISON\n"
                "══════════════════════════════\n\n"

                f"{country1}\n"
                f"Original budget: "
                f"{budget1:,.2f} {currency1}\n"
                f"Budget in home currency: "
                f"{converted1:,.2f} {home}\n"
                f"Daily limit: "
                f"{daily1:,.2f} {currency1}\n\n"

                f"{country2}\n"
                f"Original budget: "
                f"{budget2:,.2f} {currency2}\n"
                f"Budget in home currency: "
                f"{converted2:,.2f} {home}\n"
                f"Daily limit: "
                f"{daily2:,.2f} {currency2}\n\n"

                f"💰 Cheaper option: {cheaper}"
            )

            self.compare_result.delete(
                "1.0",
                "end"
            )

            self.compare_result.insert(
                "1.0",
                result
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid budgets and durations."
            )

        except APIError as error:

            messagebox.showerror(
                "Currency Error",
                str(error)
            )


    # ========================================================
    # AI TAB
    # ========================================================

    def create_ai_tab(self):

        self.ai_tab = tk.Frame(
            self.notebook,
            bg=self.BG
        )

        self.notebook.add(
            self.ai_tab,
            text="  AI Advice  "
        )

        card = self.create_card(
            self.ai_tab
        )

        card.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        ttk.Label(
            card,
            text="🤖 Gemini Travel Advice",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ttk.Label(
            card,
            text=(
                "Describe your trip and let Gemini suggest "
                "a practical budget plan."
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        self.ai_input = tk.Text(
            card,
            height=8,
            font=("Segoe UI", 11),
            bg="#FBFDFC",
            relief="solid",
            bd=1,
            wrap="word"
        )

        self.ai_input.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.ai_input.insert(
            "1.0",
            "I am travelling for 7 days. "
            "My budget is 500000 NGN. "
            "Give me practical advice for "
            "accommodation, food, transport and activities."
        )

        ttk.Button(
            card,
            text="✨ Generate AI Advice",
            style="Green.TButton",
            command=self.generate_ai_advice
        ).pack(
            anchor="w",
            padx=20,
            pady=10
        )

        self.ai_output = tk.Text(
            card,
            height=16,
            font=("Segoe UI", 10),
            bg="#FBFDFC",
            fg=self.TEXT,
            relief="solid",
            bd=1,
            wrap="word"
        )

        self.ai_output.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )


    # ========================================================
    # AI ADVICE
    # ========================================================

    def generate_ai_advice(self):

        prompt = self.ai_input.get(
            "1.0",
            "end"
        ).strip()

        if not prompt:

            messagebox.showwarning(
                "Missing Information",
                "Describe your trip first."
            )

            return

        self.ai_output.delete(
            "1.0",
            "end"
        )

        self.ai_output.insert(
            "1.0",
            "🤖 Gemini is thinking...\n\n"
        )

        self.root.update_idletasks()

        try:

            advice = (
                self.gemini_service.generate_advice(
                    prompt
                )
            )

            self.ai_output.delete(
                "1.0",
                "end"
            )

            self.ai_output.insert(
                "1.0",
                advice
            )

        except APIError as error:

            self.ai_output.delete(
                "1.0",
                "end"
            )

            self.ai_output.insert(
                "1.0",
                "Gemini is not available yet.\n\n"
                f"{error}\n\n"
                "Make sure your GEMINI_API_KEY is "
                "configured correctly."
            )


    # ========================================================
    # SET RESULT
    # ========================================================

    def set_result(self, text):

        self.result_text.config(
            state="normal"
        )

        self.result_text.delete(
            "1.0",
            "end"
        )

        self.result_text.insert(
            "1.0",
            text
        )

        self.result_text.config(
            state="disabled"
        )


    # ========================================================
    # WELCOME MESSAGE
    # ========================================================

    def show_welcome(self):

        self.set_result(
            "✈ WELCOME TO TRAVEL BUDGET PLANNER\n"
            "══════════════════════════════════\n\n"
            "Start by entering your trip details above.\n\n"
            "✓ Select your destination\n"
            "✓ Select your currencies\n"
            "✓ Enter your budget\n"
            "✓ Enter travel duration\n"
            "✓ Check public holidays\n"
            "✓ Track your expenses\n"
            "✓ Compare countries\n"
            "✓ Ask Gemini for travel advice\n\n"
            "Your trip data can also be saved as "
            "JSON and CSV files."
        )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = TravelBudgetApp(
        root
    )

    root.mainloop()