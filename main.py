import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import load_config
from handlers import setup_routers
from keep_alive import keep_alive

# Функция для установки команд в меню Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота / Начать заново"),
        BotCommand(command="reset", description="Сменить имя"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    # Запускаем Flask для Render
    keep_alive() 

    config = load_config()

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    
    # Устанавливаем меню с командами
    await set_commands(bot)

    dp = Dispatcher()
    dp["config"] = config
    dp.include_router(setup_routers())

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
