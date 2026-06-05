import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    api_id: int
    api_hash: str
    session_name: str = "user_session"


def load_config() -> AppConfig:
    load_dotenv()

    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    if not api_id or not api_hash:
        raise RuntimeError("Error: Specify API_ID and API_HASH in the .env file")

    return AppConfig(api_id=int(api_id), api_hash=api_hash)
