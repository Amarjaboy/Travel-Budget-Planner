import os
import requests


class APIError(Exception):
    """Raised when an external API operation fails."""


class HolidayService:
    BASE_URL = "https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"

    def get_holidays(self, year, country_code):
        country_code = country_code.strip().upper()

        if len(country_code) != 2 or not country_code.isalpha():
            raise APIError("Country code must be a 2-letter ISO code, e.g. NG, US or GB.")

        try:
            response = requests.get(
                self.BASE_URL.format(year=year, country_code=country_code),
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise APIError(f"Could not contact holiday service: {exc}") from exc
        except ValueError as exc:
            raise APIError("Holiday service returned invalid JSON.") from exc

        if not isinstance(data, list):
            raise APIError("Unexpected holiday data received.")
        return data

    def get_holidays_for_range(self, country_code, year, start_date, end_date):
        holidays = self.get_holidays(year, country_code)

        # A trip can cross New Year, so also check the following year.
        if start_date.year != end_date.year:
            holidays += self.get_holidays(end_date.year, country_code)

        selected = []
        for holiday in holidays:
            try:
                holiday_date = __import__("datetime").date.fromisoformat(holiday["date"])
            except (KeyError, ValueError):
                continue

            if start_date <= holiday_date <= end_date:
                selected.append({
                    "date": holiday["date"],
                    "name": holiday.get("localName") or holiday.get("name", "Public Holiday")
                })
        return selected

class GeminiService:

    API_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.7-flash"
        ).strip()

    def generate_advice(self, prompt):

        # Check if API key exists
        if not self.api_key:
            raise APIError(
                "GEMINI_API_KEY has not been configured."
            )

        # Prepare the request
        payload = {
            "model": self.model,
            "input": (
                "You are a helpful travel budgeting assistant.\n\n"
                "Give practical and realistic travel budgeting advice.\n"
                "Consider accommodation, food, transportation, "
                "activities and emergency money.\n"
                "Organize your answer clearly.\n"
                "Do not invent exact prices unless the user provides them.\n\n"
                "User request:\n"
                + prompt
            )
        }

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

        try:

            response = requests.post(
                self.API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

        except requests.exceptions.HTTPError as exc:

            # Try to show Google's actual error message
            try:
                error_data = response.json()
                error_message = error_data.get(
                    "error",
                    {}
                ).get(
                    "message",
                    str(exc)
                )
            except Exception:
                error_message = str(exc)

            raise APIError(
                f"Gemini API error: {error_message}"
            ) from exc

        except requests.exceptions.RequestException as exc:

            raise APIError(
                f"Could not connect to Gemini: {exc}"
            ) from exc

        except ValueError as exc:

            raise APIError(
                "Gemini returned invalid JSON."
            ) from exc

        # Extract the generated text
        try:

            steps = data.get("steps", [])

            for step in steps:

                if step.get("type") == "model_output":

                    content = step.get("content", [])

                    for item in content:

                        if item.get("type") == "text":

                            return item.get("text", "").strip()

            raise APIError(
                "Gemini returned no usable advice."
            )

        except (AttributeError, TypeError) as exc:

            raise APIError(
                "Gemini returned an unexpected response."
            ) from exc