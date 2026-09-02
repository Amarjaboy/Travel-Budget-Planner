from datetime import date

import requests


class HolidayError(Exception):
    """Raised when a public holiday lookup fails."""


class HolidayService:

    BASE_URL = (
        "https://date.nager.at/api/v3/PublicHolidays/"
        "{year}/{country_code}"
    )

    def get_holidays(self, year, country_code):

        country_code = country_code.strip().upper()

        if len(country_code) != 2 or not country_code.isalpha():
            raise HolidayError("Country code must be a 2-letter ISO code, e.g. NG, US or GB.")

        try:
            response = requests.get(
                self.BASE_URL.format(year=year, country_code=country_code),
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, list):
                raise HolidayError("Unexpected holiday data received.")

            return data

        except requests.RequestException as error:
            raise HolidayError(f"Could not connect to public holiday service:\n{error}") from error

        except ValueError as error:
            raise HolidayError("The public holiday service returned invalid data.") from error

    def check_range(self, start_date, end_date, country_code):
        """
        Checks every day of the trip (start_date to end_date inclusive)
        against public holidays, not just the first day.
        Returns a list of {"date": ..., "name": ...} dicts, one per holiday found.
        """

        holidays = self.get_holidays(start_date.year, country_code)

        # A trip can cross into a new year, so also check that year.
        if end_date.year != start_date.year:
            holidays += self.get_holidays(end_date.year, country_code)

        matches = []

        for holiday in holidays:

            try:
                holiday_date = date.fromisoformat(holiday["date"])
            except (KeyError, ValueError):
                continue

            if start_date <= holiday_date <= end_date:
                matches.append({
                    "date": holiday["date"],
                    "name": holiday.get("localName") or holiday.get("name") or "Public Holiday"
                })

        return matches
