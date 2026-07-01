import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    @property
    def has_gemini_key(self) -> bool:
        return bool(self.gemini_api_key and self.gemini_api_key != "your_gemini_api_key_here")


settings = Settings()
