import re
import requests


class CurrencyError(Exception):
    """Raised when currency input or conversion fails."""


class CurrencyConverter:
    API_URL = "https://open.er-api.com/v6/latest/{base}"

    def validate_currency(self, code):
        code = code.strip().upper()
        if not re.fullmatch(r"[A-Z]{3}", code):
            raise CurrencyError(
                "Invalid currency code. Use a 3-letter code such as NGN, USD or GBP."
            )
        return code

    def get_rates(self, base):
        base = self.validate_currency(base)

        try:
            response = requests.get(self.API_URL.format(base=base), timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise CurrencyError(f"Could not contact exchange-rate service: {exc}") from exc
        except ValueError as exc:
            raise CurrencyError("The exchange-rate service returned invalid JSON.") from exc

        if data.get("result") != "success":
            raise CurrencyError(data.get("error-type", "Exchange-rate request failed."))

        rates = data.get("rates")
        if not isinstance(rates, dict):
            raise CurrencyError("Exchange-rate data is missing.")
        return rates

    def convert(self, amount, from_currency, to_currency):
        if amount < 0:
            raise CurrencyError("Amount cannot be negative.")

        source = self.validate_currency(from_currency)
        target = self.validate_currency(to_currency)

        if source == target:
            return 1.0, float(amount)

        rates = self.get_rates(source)
        if target not in rates:
            raise CurrencyError(f"No exchange-rate data was found for {target}.")

        rate = float(rates[target])
        return rate, float(amount) * rate
