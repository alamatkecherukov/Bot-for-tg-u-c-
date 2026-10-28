import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    teacher_id: int


def load_config() -> Config:
    token = os.getenv("BOT_TOKEN")
    teacher_raw = os.getenv("TEACHER_ID")

    if not token:
        raise RuntimeError("BOT_TOKEN не задан")
    if not teacher_raw:
        raise RuntimeError("TEACHER_ID не задан")

    return Config(bot_token=token, teacher_id=int(teacher_raw))
