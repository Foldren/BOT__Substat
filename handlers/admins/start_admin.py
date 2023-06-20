from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from buttons import keyboard_start_admin_configured
from filters import IsAdminFilter

rt = Router()


# Хэндлер на команду /start
@rt.message(Command(commands=["start"]), IsAdminFilter())
async def start_admin(message: Message):
    message_text = f"Добрый день {message.from_user.full_name}!👋\n\n" \
                   f"Рабочие кнопки бота:\n\n" \
                   f"1️⃣ Добавить/Изменить пользователя - введите chat_id, sub_id, пользователь добавлен/изменен 😉\n\n" \
                   f"2️⃣ Забрать доступ - выдает список добавленных пользователей, просто нажмите на нужного 👈"
    await message.answer(message_text, reply_markup=keyboard_start_admin_configured)
