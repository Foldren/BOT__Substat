from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from buttons import keyboard_start_analysts_configured
from filters import IsAnalystsFilter

rt = Router()


# Хэндлер на команду /start
@rt.message(Command(commands=["start"]), IsAnalystsFilter())
async def start_analysts(message: Message):
    message_text = f"Добрый день {message.from_user.full_name}!👋\n\n" \
                   f"Рабочие кнопки бота:\n\n" \
                   f"1️⃣ Cтатистика за день 📆\n\n" \
                   f"2️⃣ Cтатистика за неделю 📅\n\n" \
                   f"3️⃣ Cтатистика за месяц 🗓\n\n" \
                   f"После выбора периода выберите sub_id, по которому нужно вывести статистику."
    await message.answer(message_text, reply_markup=keyboard_start_analysts_configured)