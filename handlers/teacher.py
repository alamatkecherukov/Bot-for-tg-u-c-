from aiogram import F, Router
from aiogram.types import Message
from config import Config
from database import get_student_id

router = Router()

@router.message(F.reply_to_message)
async def handle_teacher_reply(message: Message, config: Config):
    if message.from_user.id != config.teacher_id:
        return

    replied_msg_id = message.reply_to_message.message_id
    student_id = await get_student_id(replied_msg_id)
    
    if student_id:
        try:
            await message.bot.copy_message(
                chat_id=student_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            await message.answer("Ответ отправлен ученику ✅")
        except Exception as e:
            await message.answer("Не удалось отправить ответ (возможно, ученик заблокировал бота).")
    else:
        await message.answer("Не нашел ученика для этого сообщения. Возможно, это старое сообщение.")
