import os
import requests


class GeminiError(Exception):
    """Raised when a Gemini AI advice request fails."""


class GeminiService:

    API_URL = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/{model}:generateContent"
    )

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()

        # Use Gemini 3.6 Flash by default
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash"
        ).strip()

    def generate_advice(self, prompt):

        if not self.api_key:
            raise GeminiError(
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
                                "Give practical and realistic travel budget "
                                "advice.\n"
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
                self.API_URL.format(model=self.model),
                headers=headers,
                json=payload,
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

        except requests.Timeout as error:
            raise GeminiError(
                "Gemini took too long to respond. "
                "Please check your internet connection and try again."
            ) from error

        except requests.HTTPError as error:
            try:
                error_data = response.json()
                message = error_data.get("error", {}).get(
                    "message",
                    "Gemini API request failed."
                )
            except ValueError:
                message = "Gemini API request failed."

            raise GeminiError(
                f"Gemini API error ({response.status_code}):\n{message}"
            ) from error

        except requests.RequestException as error:
            raise GeminiError(
                f"Gemini request failed:\n{error}"
            ) from error

        except ValueError as error:
            raise GeminiError(
                "Gemini returned invalid JSON."
            ) from error

        candidates = data.get("candidates", [])

        if not candidates:
            raise GeminiError(
                "Gemini returned no response."
            )

        parts = candidates[0].get(
            "content", {}
        ).get("parts", [])

        text = "".join(
            part.get("text", "")
            for part in parts
        ).strip()

        if not text:
            raise GeminiError(
                "Gemini returned no usable advice."
            )

        return text