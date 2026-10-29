import logging
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import Config
from states import AskFlow
from database import save_message

router = Router()

def is_teacher(user_id: int, config: Config) -> bool:
    return user_id == config.teacher_id

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, config: Config) -> None:
    if is_teacher(message.from_user.id, config):
        await state.clear()
        await message.answer("Привет! Ты вошел как учитель. Сюда будут приходить вопросы от учеников.")
        return

    await state.clear()
    await state.set_state(AskFlow.waiting_name)
    await message.answer(
        "Привет! Это бот для вопросов учителю.\n\n"
        "Как тебя зовут?"
    )

@router.message(Command("reset"))
async def cmd_reset(message: Message, state: FSMContext, config: Config) -> None:
    if is_teacher(message.from_user.id, config):
        await message.answer("Тебе не нужно сбрасывать имя, ты учитель.")
        return

    await state.clear()
    await state.set_state(AskFlow.waiting_name)
    await message.answer("Ок, начнём заново. Как тебя зовут?")

@router.message(AskFlow.waiting_name, F.text)
async def set_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip()
    
    if len(name) < 2:
        await message.answer("Имя слишком короткое, напиши ещё раз.")
        return
    if len(name) > 100:
        await message.answer("Слишком длинно, напиши покороче.")
        return

    await state.update_data(name=name)
    await state.set_state(AskFlow.asking)
    await message.answer(
        f"Приятно познакомиться, {name}!\n\n"
        "Теперь можешь задать вопрос — текстом, фото, видео, голосовым, документом, чем угодно.\n"
        "Чтобы сменить имя — /reset"
    )

@router.message(AskFlow.waiting_name)
async def set_name_wrong(message: Message) -> None:
    await message.answer("Пожалуйста, напиши имя текстом.")

@router.message(AskFlow.asking)
async def forward_question(message: Message, state: FSMContext, config: Config) -> None:
    if is_teacher(message.from_user.id, config):
        await message.answer("Ты учитель, твои сообщения не пересылаются.")
        return

    data = await state.get_data()
    name = data.get("name", "Без имени")
    username = f"@{message.from_user.username}" if message.from_user.username else "—"
    header = f"<b>{name}</b> ({username})"
    
    try:
        await message.bot.send_message(config.teacher_id, header)
        sent_msg = await message.bot.copy_message(
            chat_id=config.teacher_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        await save_message(sent_msg.message_id, message.from_user.id)
        await message.answer("Вопрос отправлен учителю ✅\nМожешь задать следующий или нажать /reset.")
    except Exception as e:
        logging.error(f"Ошибка отправки учителю: {e}")
        await message.answer("Не удалось отправить вопрос. Попробуй позже.")
