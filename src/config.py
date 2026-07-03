import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    @property
    def has_gemini_key(self) -> bool:
        return bool(
            self.gemini_api_key
            and self.gemini_api_key != "your_gemini_api_key_here"
        )

    def require_gemini(self):
        if not self.has_gemini_key:
            raise ValueError(
                "Gemini mode requires GEMINI_API_KEY in .env"
            )

settings = Settings()