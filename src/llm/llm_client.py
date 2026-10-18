
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.8-flash"

MAX_ATTEMPTS = 3
RETRY_DELAYS = [2, 4]

# Temporary server or rate-limit errors that may recover.
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def generate_response(prompt):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            if not response.text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            return response.text.strip()

        except (errors.APIError, Exception) as error:
            status_code = getattr(error, "code", None)

            # Do not retry ordinary programming errors,
            # authentication errors, or invalid requests.
            if status_code not in RETRYABLE_STATUS_CODES:
                print(f"Gemini API error: {error}")
                raise

            if attempt == MAX_ATTEMPTS:
                print(
                    f"Gemini remained unavailable after "
                    f"{MAX_ATTEMPTS} attempts: {error}"
                )
                raise

            delay = RETRY_DELAYS[attempt - 1]

            print(
                f"Gemini is temporarily busy "
                f"(HTTP {status_code}). "
                f"Retrying in {delay} seconds "
                f"(attempt {attempt + 1}/{MAX_ATTEMPTS})..."
            )

            time.sleep(delay)

    raise RuntimeError("Gemini could not complete the request.")
