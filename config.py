import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    bot_token: str
    teacher_id: int  # Снова просто число

def load_config() -> Config:
    token = os.getenv("BOT_TOKEN", "").strip()
    teacher_raw = os.getenv("TEACHER_ID", "").strip() # Ищем TEACHER_ID

    if not token:
        raise RuntimeError("BOT_TOKEN не задан или пустой")
    
    if not teacher_raw:
        raise RuntimeError("TEACHER_ID не задан.")

    try:
        # Если вдруг там несколько ID через запятую, берем первый
        teacher_id = int(teacher_raw.split(",")[0].strip())
    except ValueError:
        raise RuntimeError(f"TEACHER_ID должен быть числом, а пришло: '{teacher_raw}'")

    return Config(bot_token=token, teacher_id=teacher_id)
