import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    bot_token: str
    teacher_id: int

def load_config() -> Config:
    # .strip() убирает случайные пробелы, которые часто появляются при копировании на Render
    token = os.getenv("BOT_TOKEN", "").strip()
    teacher_raw = os.getenv("TEACHER_ID", "").strip()

    if not token:
        raise RuntimeError("BOT_TOKEN не задан или пустой")
    
    if not teacher_raw:
        raise RuntimeError("TEACHER_ID не задан или пустой. Добавь его в Environment Variables на Render.")

    try:
        teacher_id = int(teacher_raw)
    except ValueError:
        raise RuntimeError(f"TEACHER_ID должен быть числом (ID из @userinfobot), а пришло: '{teacher_raw}'")

    return Config(bot_token=token, teacher_id=teacher_id)
