from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import Config
from states import AskFlow

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(AskFlow.waiting_name)
    await message.answer(
        "Привет! Это бот для вопросов учителю.\n\n"
        "Как тебя зовут? Напиши имя и фамилию (например: Иван Петров)."
    )


@router.message(Command("reset"))
async def cmd_reset(message: Message, state: FSMContext) -> None:
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


# Ловим вообще всё, что приходит в состоянии asking
@router.message(AskFlow.asking)
async def forward_question(message: Message, state: FSMContext, config: Config) -> None:
    data = await state.get_data()
    name = data.get("name", "Без имени")
    username = f"@{message.from_user.username}" if message.from_user.username else "—"
    user_id = message.from_user.id

    header = (
        f"📩 Новый вопрос\n"
        f"👤 Имя: {name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 ID: {user_id}"
    )

    # Заголовок отдельным сообщением — чтобы не потерялся в пересылке
    await message.bot.send_message(config.teacher_id, header)

    # Пересылаем само сообщение как есть (сохраняет формат: фото, видео, голос, документ, стикер и т.д.)
    await message.forward(config.teacher_id)

    await message.answer("Вопрос отправлен учителю ✅\nМожешь задать следующий или нажать /reset, чтобы сменить имя.")
