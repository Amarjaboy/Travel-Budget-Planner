import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

from currency_converter import CurrencyConverter, CurrencyError
from trip_budget import TripBudget, TripBudgetError
from expense import Expense
from budget_report import BudgetReport
from holiday_service import HolidayService, HolidayError
from gemini_service import GeminiService, GeminiError


# ============================================================
# COUNTRY LIST
# ============================================================

COUNTRIES = {
    "Afghanistan": "AF",
    "Albania": "AL",
    "Algeria": "DZ",
    "Andorra": "AD",
    "Angola": "AO",
    "Antigua and Barbuda": "AG",
    "Argentina": "AR",
    "Armenia": "AM",
    "Australia": "AU",
    "Austria": "AT",
    "Azerbaijan": "AZ",
    "Bahamas": "BS",
    "Bahrain": "BH",
    "Bangladesh": "BD",
    "Barbados": "BB",
    "Belarus": "BY",
    "Belgium": "BE",
    "Belize": "BZ",
    "Benin": "BJ",
    "Bhutan": "BT",
    "Bolivia": "BO",
    "Bosnia and Herzegovina": "BA",
    "Botswana": "BW",
    "Brazil": "BR",
    "Brunei": "BN",
    "Bulgaria": "BG",
    "Burkina Faso": "BF",
    "Burundi": "BI",
    "Cabo Verde": "CV",
    "Cambodia": "KH",
    "Cameroon": "CM",
    "Canada": "CA",
    "Central African Republic": "CF",
    "Chad": "TD",
    "Chile": "CL",
    "China": "CN",
    "Colombia": "CO",
    "Comoros": "KM",
    "Congo": "CG",
    "Costa Rica": "CR",
    "Croatia": "HR",
    "Cuba": "CU",
    "Cyprus": "CY",
    "Czechia": "CZ",
    "Democratic Republic of the Congo": "CD",
    "Denmark": "DK",
    "Djibouti": "DJ",
    "Dominica": "DM",
    "Dominican Republic": "DO",
    "Ecuador": "EC",
    "Egypt": "EG",
    "El Salvador": "SV",
    "Equatorial Guinea": "GQ",
    "Eritrea": "ER",
    "Estonia": "EE",
    "Eswatini": "SZ",
    "Ethiopia": "ET",
    "Fiji": "FJ",
    "Finland": "FI",
    "France": "FR",
    "Gabon": "GA",
    "Gambia": "GM",
    "Georgia": "GE",
    "Germany": "DE",
    "Ghana": "GH",
    "Greece": "GR",
    "Grenada": "GD",
    "Guatemala": "GT",
    "Guinea": "GN",
    "Guinea-Bissau": "GW",
    "Guyana": "GY",
    "Haiti": "HT",
    "Honduras": "HN",
    "Hungary": "HU",
    "Iceland": "IS",
    "India": "IN",
    "Indonesia": "ID",
    "Iran": "IR",
    "Iraq": "IQ",
    "Ireland": "IE",
    "Israel": "IL",
    "Italy": "IT",
    "Jamaica": "JM",
    "Japan": "JP",
    "Jordan": "JO",
    "Kazakhstan": "KZ",
    "Kenya": "KE",
    "Kiribati": "KI",
    "Kuwait": "KW",
    "Kyrgyzstan": "KG",
    "Laos": "LA",
    "Latvia": "LV",
    "Lebanon": "LB",
    "Lesotho": "LS",
    "Liberia": "LR",
    "Libya": "LY",
    "Liechtenstein": "LI",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Madagascar": "MG",
    "Malawi": "MW",
    "Malaysia": "MY",
    "Maldives": "MV",
    "Mali": "ML",
    "Malta": "MT",
    "Marshall Islands": "MH",
    "Mauritania": "MR",
    "Mauritius": "MU",
    "Mexico": "MX",
    "Micronesia": "FM",
    "Moldova": "MD",
    "Monaco": "MC",
    "Mongolia": "MN",
    "Montenegro": "ME",
    "Morocco": "MA",
    "Mozambique": "MZ",
    "Myanmar": "MM",
    "Namibia": "NA",
    "Nauru": "NR",
    "Nepal": "NP",
    "Netherlands": "NL",
    "New Zealand": "NZ",
    "Nicaragua": "NI",
    "Niger": "NE",
    "Nigeria": "NG",
    "North Korea": "KP",
    "North Macedonia": "MK",
    "Norway": "NO",
    "Oman": "OM",
    "Pakistan": "PK",
    "Palau": "PW",
    "Palestine": "PS",
    "Panama": "PA",
    "Papua New Guinea": "PG",
    "Paraguay": "PY",
    "Peru": "PE",
    "Philippines": "PH",
    "Poland": "PL",
    "Portugal": "PT",
    "Qatar": "QA",
    "Romania": "RO",
    "Russia": "RU",
    "Rwanda": "RW",
    "Saint Kitts and Nevis": "KN",
    "Saint Lucia": "LC",
    "Saint Vincent and the Grenadines": "VC",
    "Samoa": "WS",
    "San Marino": "SM",
    "Sao Tome and Principe": "ST",
    "Saudi Arabia": "SA",
    "Senegal": "SN",
    "Serbia": "RS",
    "Seychelles": "SC",
    "Sierra Leone": "SL",
    "Singapore": "SG",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Solomon Islands": "SB",
    "Somalia": "SO",
    "South Africa": "ZA",
    "South Korea": "KR",
    "South Sudan": "SS",
    "Spain": "ES",
    "Sri Lanka": "LK",
    "Sudan": "SD",
    "Suriname": "SR",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Syria": "SY",
    "Tajikistan": "TJ",
    "Tanzania": "TZ",
    "Thailand": "TH",
    "Timor-Leste": "TL",
    "Togo": "TG",
    "Tonga": "TO",
    "Trinidad and Tobago": "TT",
    "Tunisia": "TN",
    "Turkey": "TR",
    "Turkmenistan": "TM",
    "Tuvalu": "TV",
    "Uganda": "UG",
    "Ukraine": "UA",
    "United Arab Emirates": "AE",
    "United Kingdom": "GB",
    "United States": "US",
    "Uruguay": "UY",
    "Uzbekistan": "UZ",
    "Vanuatu": "VU",
    "Vatican City": "VA",
    "Venezuela": "VE",
    "Vietnam": "VN",
    "Yemen": "YE",
    "Zambia": "ZM",
    "Zimbabwe": "ZW",
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
    "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SOS",
    "SRD", "SSP", "STN", "SYP", "SZL", "THB", "TJS", "TMT",
    "TND", "TOP", "TRY", "TTD", "TVD", "TWD", "TZS", "UAH",
    "UGX", "USD", "UYU", "UZS", "VES", "VND", "VUV", "WST",
    "XAF", "XCD", "XOF", "XPF", "YER", "ZAR", "ZMW", "ZWL"
]


# ============================================================
# MAIN APPLICATION
# ============================================================

class TravelBudgetApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Travel Budget Planner")
        self.root.geometry("1200x760")
        self.root.minsize(1000, 650)

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

        self.root.configure(bg=self.BG)

        # ----------------------------------------------------
        # SERVICES
        # ----------------------------------------------------

        self.currency_converter = CurrencyConverter()
        self.holiday_service = HolidayService()
        self.gemini_service = GeminiService()

        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        self.destination_country = tk.StringVar()
        self.destination_code = tk.StringVar()

        self.home_currency = tk.StringVar(value="NGN")
        self.destination_currency = tk.StringVar(value="USD")

        self.amount = tk.StringVar()
        self.start_date = tk.StringVar()
        self.duration = tk.StringVar()
        self.end_date = tk.StringVar()

        self.current_trip = None
        self.converted_budget = 0.0

        self.expenses = []

        # ----------------------------------------------------
        # STYLE + LAYOUT
        # ----------------------------------------------------

        self.setup_styles()

        self.create_header()
        self.create_notebook()

        self.create_trip_tab()
        self.create_currency_tab()
        self.create_price_tab()
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

        style.configure("TNotebook", background=self.BG, borderwidth=0)

        style.configure(
            "TNotebook.Tab",
            padding=(20, 12),
            font=("Segoe UI", 10, "bold"),
            background="#E5E7EB"
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", self.GREEN)],
            foreground=[("selected", self.WHITE)]
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
            font=("Segoe UI", 24, "bold")
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
            background=[("active", self.DARK_GREEN)]
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
            background=[("active", "#B89625")]
        )

        style.configure("TEntry", padding=8)
        style.configure("TCombobox", padding=7)

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(self.root, bg=self.GREEN, height=115)
        header.pack(fill="x")
        header.pack_propagate(False)

        ttk.Label(
            header,
            text="TRAVEL BUDGET PLANNER",
            style="Title.TLabel"
        ).pack(pady=(20, 2))

        ttk.Label(
            header,
            text="Plan Smart  •  Track Expenses  •  Travel Better",
            style="Subtitle.TLabel"
        ).pack()

    # ========================================================
    # NOTEBOOK / CARD HELPERS
    # ========================================================

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=15)

    def create_card(self, parent):
        return tk.Frame(parent, bg=self.WHITE, bd=1, relief="solid")

    def set_text(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.config(state="disabled")

    # ========================================================
    # TRIP BUDGET TAB
    # ========================================================

    def create_trip_tab(self):

        self.trip_tab = tk.Frame(self.notebook, bg=self.BG)
        self.notebook.add(self.trip_tab, text="  Trip Budget  ")

        card = self.create_card(self.trip_tab)
        card.pack(fill="x", padx=10, pady=10)

        ttk.Label(
            card,
            text="Trip Details",
            style="Section.TLabel"
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            padx=20,
            pady=(18, 15)
        )

        # Destination country + code
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
            width=28
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

        ttk.Entry(
            card,
            textvariable=self.destination_code,
            width=15
        ).grid(
            row=1,
            column=3,
            padx=10
        )

        # Currencies
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

        ttk.Combobox(
            card,
            textvariable=self.home_currency,
            values=CURRENCIES,
            state="readonly",
            width=28
        ).grid(
            row=2,
            column=1,
            padx=10
        )

        ttk.Label(
            card,
            text="Destination currency:"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=20
        )

        ttk.Combobox(
            card,
            textvariable=self.destination_currency,
            values=CURRENCIES,
            state="readonly",
            width=15
        ).grid(
            row=2,
            column=3,
            padx=10
        )

        # Budget
        ttk.Label(
            card,
            text="Travel budget (home currency):"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=8
        )

        ttk.Entry(
            card,
            textvariable=self.amount,
            width=30
        ).grid(
            row=3,
            column=1,
            padx=10
        )

        # Start date
        ttk.Label(
            card,
            text="Travel start date (YYYY-MM-DD):"
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
            width=30
        ).grid(
            row=4,
            column=1,
            padx=10
        )

        # Duration
        ttk.Label(
            card,
            text="Duration (days):"
        ).grid(
            row=4,
            column=2,
            sticky="w",
            padx=20
        )

        ttk.Entry(
            card,
            textvariable=self.duration,
            width=17
        ).grid(
            row=4,
            column=3,
            padx=10
        )

        # End date
        ttk.Label(
            card,
            text="Travel end date:"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            padx=20,
            pady=8
        )

        ttk.Entry(
            card,
            textvariable=self.end_date,
            width=30,
            state="readonly"
        ).grid(
            row=5,
            column=1,
            padx=10
        )

        button_frame = tk.Frame(card, bg=self.WHITE)

        button_frame.grid(
            row=6,
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
            text="Save Trip + Expenses",
            command=self.save_trip
        ).pack(
            side="left",
            padx=10
        )

        result_card = self.create_card(self.trip_tab)
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

        result_frame = tk.Frame(
            result_card,
            bg=self.WHITE
        )

        result_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.result_text = tk.Text(
            result_frame,
            height=14,
            bg="#FBFDFC",
            fg=self.TEXT,
            font=("Consolas", 11),
            relief="flat",
            padx=15,
            pady=15
        )

        result_scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.result_text.yview
        )

        self.result_text.configure(
            yscrollcommand=result_scrollbar.set
        )

        self.result_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        result_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.result_text.config(state="disabled")

    def country_selected(self, event=None):
        code = COUNTRIES.get(
            self.destination_country.get(),
            ""
        )
        self.destination_code.set(code)

    def parse_trip_dates(self):

        try:
            start = datetime.strptime(
                self.start_date.get().strip(),
                "%Y-%m-%d"
            ).date()
        except ValueError as exc:
            raise TripBudgetError(
                "Start date must use YYYY-MM-DD format."
            ) from exc

        try:
            duration = int(
                self.duration.get().strip()
            )

            if duration <= 0:
                raise ValueError

        except ValueError as exc:
            raise TripBudgetError(
                "Duration must be a positive whole number."
            ) from exc

        end = date.fromordinal(
            start.toordinal() + duration - 1
        )

        self.end_date.set(
            end.isoformat()
        )

        return start, end

    # ========================================================
    # CALCULATE BUDGET
    # ========================================================

    def calculate_budget(self):

        try:
            amount = float(self.amount.get())

            if amount <= 0:
                raise ValueError

            start, end = self.parse_trip_dates()

            trip = TripBudget(
                self.home_currency.get(),
                self.destination_currency.get(),
                amount,
                start.isoformat(),
                end.isoformat(),
            )

            rate, converted = self.currency_converter.convert(
                trip.amount,
                trip.home_currency,
                trip.destination_currency
            )

            daily_limit = trip.daily_limit(converted)

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid positive budget amount and duration."
            )
            return

        except (TripBudgetError, CurrencyError) as error:
            messagebox.showerror(
                "Could Not Calculate Budget",
                str(error)
            )
            return

        self.current_trip = trip
        self.converted_budget = converted

        total_expenses = self.total_expenses_in_destination_currency()
        remaining = converted - total_expenses

        destination = (
            self.destination_country.get()
            or "Not selected"
        )

        result = (
            "TRAVEL BUDGET SUMMARY\n"
            "══════════════════════════════\n\n"
            f"Destination: {destination}\n"
            f"Budget: {trip.amount:,.2f} {trip.home_currency}\n"
            f"Exchange rate used: 1 {trip.home_currency} = "
            f"{rate:.4f} {trip.destination_currency}\n"
            f"Budget in destination currency: "
            f"{converted:,.2f} {trip.destination_currency}\n"
            f"Trip duration: {trip.duration_days} day(s)\n"
            f"Start date: {trip.start_date.isoformat()}\n"
            f"End date: {trip.end_date.isoformat()}\n"
            f"Daily limit: {daily_limit:,.2f} "
            f"{trip.destination_currency}\n\n"
            "EXPENSES\n"
            "──────────────────────────────\n"
            f"Total expenses: {total_expenses:,.2f} "
            f"{trip.destination_currency}\n"
            f"Remaining budget: {remaining:,.2f} "
            f"{trip.destination_currency}\n"
        )

        if remaining < 0:
            result += (
                "\nWARNING: Your expenses are above your budget."
            )
        else:
            result += (
                "\nSTATUS: Your current expenses are within budget."
            )

        self.set_text(
            self.result_text,
            result
        )

    def total_expenses_in_destination_currency(self):

        if not self.current_trip or not self.expenses:
            return 0.0

        total = 0.0
        destination = self.current_trip.destination_currency

        for expense in self.expenses:

            try:
                _, converted = self.currency_converter.convert(
                    expense.amount,
                    expense.currency,
                    destination
                )

                total += converted

            except CurrencyError:
                continue

        return total

    # ========================================================
    # PUBLIC HOLIDAYS
    # ========================================================

    def check_holidays(self):

        country_code = (
            self.destination_code.get()
            .strip()
            .upper()
        )

        try:
            start, end = self.parse_trip_dates()

        except TripBudgetError as error:
            messagebox.showerror(
                "Invalid Dates",
                str(error)
            )
            return

        if end < start:
            messagebox.showerror(
                "Invalid Dates",
                "End date cannot be before start date."
            )
            return

        if len(country_code) != 2:
            messagebox.showerror(
                "Country Code",
                "Country code must contain 2 letters."
            )
            return

        try:
            holidays = self.holiday_service.check_range(
                start,
                end,
                country_code
            )

        except HolidayError as error:
            messagebox.showwarning(
                "Holiday Service",
                f"{error}\n\n"
                "The program can continue, but holiday status "
                "could not be confirmed."
            )
            return

        if holidays:

            lines = "\n".join(
                f"  - {h['date']}: {h['name']}"
                for h in holidays
            )

            self.set_text(
                self.result_text,
                "PUBLIC HOLIDAY WARNING\n"
                "══════════════════════════════\n\n"
                f"{len(holidays)} public holiday(s) "
                "fall within your trip:\n\n"
                f"{lines}\n\n"
                "You may want to plan around these dates."
            )

            messagebox.showwarning(
                "Public Holidays Found",
                f"{len(holidays)} holiday(s) "
                "fall within your trip."
            )

        else:

            self.set_text(
                self.result_text,
                "TRAVEL DATES CLEAR\n"
                "══════════════════════════════\n\n"
                f"No public holidays were found between "
                f"{start.isoformat()} and {end.isoformat()}."
            )

            messagebox.showinfo(
                "No Holidays Found",
                "No public holidays fall within your trip dates."
            )

    # ========================================================
    # SAVE TRIP
    # ========================================================

    def save_trip(self):

        if not self.current_trip:
            messagebox.showwarning(
                "Nothing to Save",
                "Calculate a budget first."
            )
            return

        try:

            BudgetReport.save_trip_json(
                self.current_trip,
                "trip.json"
            )

            if self.expenses:

                BudgetReport.save_expenses_json(
                    self.expenses,
                    "expenses.json"
                )

                BudgetReport.export_expenses_csv(
                    self.expenses,
                    "expenses.csv"
                )

            messagebox.showinfo(
                "Saved",
                "Trip and expenses saved successfully."
            )

        except OSError as error:
            messagebox.showerror(
                "Save Error",
                str(error)
            )

    # ========================================================
    # CURRENCY CONVERTER TAB
    # ========================================================

    def create_currency_tab(self):

        self.currency_tab = tk.Frame(
            self.notebook,
            bg=self.BG
        )

        self.notebook.add(
            self.currency_tab,
            text="  Currency Converter  "
        )

        card = self.create_card(
            self.currency_tab
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

        from_combo.set("NGN")
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

        to_combo.set("USD")
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

                rate, result = self.currency_converter.convert(
                    amount,
                    from_combo.get(),
                    to_combo.get()
                )

                result_label.config(
                    text=(
                        f"{amount:,.2f} "
                        f"{from_combo.get()} = "
                        f"{result:,.2f} "
                        f"{to_combo.get()} "
                        f"(rate: {rate:.4f})"
                    ),
                    foreground=self.GREEN
                )

            except ValueError:
                result_label.config(
                    text="Enter a valid amount.",
                    foreground=self.RED
                )

            except CurrencyError as error:
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
    # PRICE EXTRACTOR TAB
    # ========================================================

    def create_price_tab(self):

        self.price_tab = tk.Frame(
            self.notebook,
            bg=self.BG
        )

        self.notebook.add(
            self.price_tab,
            text="  Price Extractor  "
        )

        card = self.create_card(
            self.price_tab
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
            text="Example: Hotel 80,000, Food 30,000, Transport 12,500.50"
        ).pack(
            anchor="w",
            padx=20
        )

        entry = ttk.Entry(card)

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

            prices = self.currency_converter.extract_prices(
                entry.get()
            )

            result.config(
                text=(
                    f"Extracted prices: {prices}  "
                    f"(total: {sum(prices):,.2f})"
                )
            )

        ttk.Button(
            card,
            text="Extract Prices",
            style="Green.TButton",
            command=extract
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
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
            text="Date (YYYY-MM-DD):"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.expense_date = ttk.Entry(
            form,
            width=14
        )

        self.expense_date.insert(
            0,
            date.today().isoformat()
        )

        self.expense_date.grid(
            row=0,
            column=1,
            padx=10
        )

        ttk.Label(
            form,
            text="Category:"
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.expense_category = ttk.Entry(
            form,
            width=16
        )

        self.expense_category.grid(
            row=0,
            column=3,
            padx=10
        )

        ttk.Label(
            form,
            text="Description:"
        ).grid(
            row=0,
            column=4,
            padx=5
        )

        self.expense_description = ttk.Entry(
            form,
            width=20
        )

        self.expense_description.grid(
            row=0,
            column=5,
            padx=10
        )

        ttk.Label(
            form,
            text="Amount:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=8
        )

        self.expense_amount = ttk.Entry(
            form,
            width=14
        )

        self.expense_amount.grid(
            row=1,
            column=1,
            padx=10
        )

        ttk.Label(
            form,
            text="Currency:"
        ).grid(
            row=1,
            column=2,
            padx=5
        )

        self.expense_currency = ttk.Combobox(
            form,
            values=CURRENCIES,
            state="readonly",
            width=13
        )

        self.expense_currency.set(
            self.destination_currency.get()
        )

        self.expense_currency.grid(
            row=1,
            column=3,
            padx=10
        )

        ttk.Button(
            form,
            text="Add Expense",
            style="Green.TButton",
            command=self.add_expense
        ).grid(
            row=1,
            column=5,
            padx=10
        )

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
            "date",
            "category",
            "description",
            "amount",
            "currency"
        )

        self.expense_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        for col, width in zip(
            columns,
            (100, 130, 220, 110, 90)
        ):

            self.expense_tree.heading(
                col,
                text=col.capitalize()
            )

            self.expense_tree.column(
                col,
                width=width
            )

        expense_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.expense_tree.yview
        )

        self.expense_tree.configure(
            yscrollcommand=expense_scrollbar.set
        )

        self.expense_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        expense_scrollbar.pack(
            side="right",
            fill="y"
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

    def add_expense(self):

        try:

            expense = Expense(
                date=self.expense_date.get().strip(),
                category=self.expense_category.get().strip(),
                description=self.expense_description.get().strip(),
                amount=float(
                    self.expense_amount.get() or 0
                ),
                currency=(
                    self.expense_currency.get()
                    or self.destination_currency.get()
                ),
            )

        except ValueError as error:

            messagebox.showerror(
                "Invalid Expense",
                str(error)
            )

            return

        self.expenses.append(expense)

        self.expense_tree.insert(
            "",
            "end",
            values=(
                expense.date,
                expense.category,
                expense.description,
                f"{expense.amount:,.2f}",
                expense.currency
            )
        )

        self.refresh_expense_total()

        self.expense_category.delete(
            0,
            "end"
        )

        self.expense_description.delete(
            0,
            "end"
        )

        self.expense_amount.delete(
            0,
            "end"
        )

    def delete_expense(self):

        selected = self.expense_tree.selection()

        if not selected:
            return

        for item in selected:

            index = self.expense_tree.index(item)

            del self.expenses[index]

            self.expense_tree.delete(item)

        self.refresh_expense_total()

    def clear_expenses(self):

        self.expenses.clear()

        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)

        self.refresh_expense_total()

    def refresh_expense_total(self):

        total = sum(
            expense.amount
            for expense in self.expenses
        )

        self.expense_total_label.config(
            text=f"Total: {total:,.2f}"
        )

    def save_expenses(self):

        if not self.expenses:

            messagebox.showwarning(
                "No Expenses",
                "There are no expenses to save."
            )

            return

        try:

            BudgetReport.save_expenses_json(
                self.expenses,
                "expenses.json"
            )

            BudgetReport.export_expenses_csv(
                self.expenses,
                "expenses.csv"
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
    # COMPARE COUNTRIES TAB
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

        self.compare_home.set("NGN")

        self.compare_home.grid(
            row=1,
            column=1
        )

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

        compare_result_frame = tk.Frame(
            result_card,
            bg=self.WHITE
        )

        compare_result_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.compare_result = tk.Text(
            compare_result_frame,
            bg="#FBFDFC",
            fg=self.TEXT,
            font=("Consolas", 11),
            relief="flat",
            padx=15,
            pady=15
        )

        compare_scrollbar = ttk.Scrollbar(
            compare_result_frame,
            orient="vertical",
            command=self.compare_result.yview
        )

        self.compare_result.configure(
            yscrollcommand=compare_scrollbar.set
        )

        self.compare_result.pack(
            side="left",
            fill="both",
            expand=True
        )

        compare_scrollbar.pack(
            side="right",
            fill="y"
        )

    def compare_countries(self):

        try:

            home = self.compare_home.get()

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

            currency1 = self.compare_currency1.get()
            currency2 = self.compare_currency2.get()

            _, converted1 = self.currency_converter.convert(
                budget1,
                currency1,
                home
            )

            _, converted2 = self.currency_converter.convert(
                budget2,
                currency2,
                home
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid budgets and durations."
            )

            return

        except CurrencyError as error:

            messagebox.showerror(
                "Currency Error",
                str(error)
            )

            return

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
            "TRAVEL COMPARISON\n"
            "══════════════════════════════\n\n"
            f"{country1}\n"
            f"Original budget: {budget1:,.2f} {currency1}\n"
            f"Budget in home currency: {converted1:,.2f} {home}\n"
            f"Daily limit: {daily1:,.2f} {currency1}\n\n"
            f"{country2}\n"
            f"Original budget: {budget2:,.2f} {currency2}\n"
            f"Budget in home currency: {converted2:,.2f} {home}\n"
            f"Daily limit: {daily2:,.2f} {currency2}\n\n"
            f"Cheaper option: {cheaper}"
        )

        self.compare_result.delete(
            "1.0",
            "end"
        )

        self.compare_result.insert(
            "1.0",
            result
        )

    # ========================================================
    # AI ADVICE TAB
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
            text="Gemini Travel Advice",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ttk.Label(
            card,
            text="Describe your trip and let Gemini suggest a practical budget plan."
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        # AI INPUT + SCROLLBAR
        ai_input_frame = tk.Frame(
            card,
            bg=self.WHITE
        )

        ai_input_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.ai_input = tk.Text(
            ai_input_frame,
            height=8,
            font=("Segoe UI", 11),
            bg="#FBFDFC",
            relief="solid",
            bd=1,
            wrap="word"
        )

        ai_input_scrollbar = ttk.Scrollbar(
            ai_input_frame,
            orient="vertical",
            command=self.ai_input.yview
        )

        self.ai_input.configure(
            yscrollcommand=ai_input_scrollbar.set
        )

        self.ai_input.pack(
            side="left",
            fill="both",
            expand=True
        )

        ai_input_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.ai_input.insert(
            "1.0",
            "I am travelling for 7 days. My budget is 500000 NGN. "
            "Give me practical advice for accommodation, food, transport and activities."
        )

        ttk.Button(
            card,
            text="Generate AI Advice",
            style="Green.TButton",
            command=self.generate_ai_advice
        ).pack(
            anchor="w",
            padx=20,
            pady=10
        )

        # AI OUTPUT + SCROLLBAR
        ai_output_frame = tk.Frame(
            card,
            bg=self.WHITE
        )

        ai_output_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.ai_output = tk.Text(
            ai_output_frame,
            height=16,
            font=("Segoe UI", 10),
            bg="#FBFDFC",
            fg=self.TEXT,
            relief="solid",
            bd=1,
            wrap="word"
        )

        ai_output_scrollbar = ttk.Scrollbar(
            ai_output_frame,
            orient="vertical",
            command=self.ai_output.yview
        )

        self.ai_output.configure(
            yscrollcommand=ai_output_scrollbar.set
        )

        self.ai_output.pack(
            side="left",
            fill="both",
            expand=True
        )

        ai_output_scrollbar.pack(
            side="right",
            fill="y"
        )

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
            "Gemini is thinking...\n\n"
        )

        self.root.update_idletasks()

        try:

            advice = self.gemini_service.generate_advice(
                prompt
            )

            self.ai_output.delete(
                "1.0",
                "end"
            )

            self.ai_output.insert(
                "1.0",
                advice
            )

        except GeminiError as error:

            self.ai_output.delete(
                "1.0",
                "end"
            )

            self.ai_output.insert(
                "1.0",
                f"Gemini is not available right now.\n\n"
                f"{error}\n\n"
                "Make sure your GEMINI_API_KEY is configured correctly."
            )

    # ========================================================
    # WELCOME MESSAGE
    # ========================================================

    def show_welcome(self):

        self.set_text(
            self.result_text,
            "WELCOME TO TRAVEL BUDGET PLANNER\n"
            "══════════════════════════════════\n\n"
            "Start by entering your trip details above.\n\n"
            "- Select your destination\n"
            "- Select your currencies\n"
            "- Enter your budget\n"
            "- Enter your travel start date\n"
            "- Enter the duration of your trip\n"
            "- Calculate your budget\n"
            "- Check public holidays across your whole trip\n"
            "- Track your expenses\n"
            "- Compare countries\n"
            "- Ask Gemini for travel advice\n\n"
            "Your trip data can also be saved as JSON and CSV files."
        )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()
    app = TravelBudgetApp(root)
    root.mainloop()