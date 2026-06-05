from datetime import datetime
from pathlib import Path
from typing import Optional


def format_dt(value: Optional[datetime] = None) -> str:
    current = value or datetime.now().astimezone()
    if current.tzinfo is not None:
        current = current.astimezone()
    return current.strftime("%Y-%m-%d %H:%M:%S")


class ActivityLogger:
    def __init__(self, log_file: str):
        self.log_file = Path(log_file)

    def write(self, text: str) -> None:
        print(text)
        with self.log_file.open("a", encoding="utf-8") as file:
            file.write(text + "\n")

    def event(self, category: str, text: str, event_time: Optional[datetime] = None) -> None:
        self.write(f"[{format_dt(event_time)}] {category}: {text}")
