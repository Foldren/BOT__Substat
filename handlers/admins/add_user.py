from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from states.state_add_user import StepsAddUser
from aiogram import Router
from aiogram.filters import Text
from config import db_admins_cid_redis, db_analysts_cid_redis
from filters import IsAdminFilter, CheckChatIdFilter, IsAddUserFilter
from tools import SubStatTools as ST

rt = Router()
rt.message.filter(IsAdminFilter())


@rt.message(Text(text="Добавить/Изменить пользователя"))
async def get_chatsub_id(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(StepsAddUser.writing_chatsub_id)
    await message.answer("Введите 5 параметров, каждый новый параметр, начиная со второго - вводите с новой строки:\n"
                         "1️⃣ chat_id - пользователя которому нужно расшарить доступ\n"
                         "2️⃣ number_sub_id - номер sub_id который нужно установить пользователю\n"
                         "3️⃣ sub_id - значение sub_id (также если несколько, можно указать через запятую)\n"
                         "4️⃣ partner_id - id партнера\n"
                         "5️⃣ tz - таймзона (в формате 'Europe/Berlin')\n"
                         "6️⃣ geo - геолокация из двух латинских букв \n\n"
                         "Также вы можете по очереди добавлять другие номера сабов (1, 2, 3..), задавайте новый номер в новом сообщении 📨\n\n"
                         "Список доступных таймзон (графа TZ identifier) 🌍 👇👉"
                         "<a href='link'>https://en.wikipedia.org/wiki/List_of_tz_database_time_zones</a>)\n\n"
                         "Пример:<code>\n2895125056\n1\nAnna\n7466\nAmerica/Lima\nPE</code>", parse_mode='html', disable_web_page_preview=True)

@rt.message(StepsAddUser.writing_chatsub_id, IsAddUserFilter(), CheckChatIdFilter())
async def add_chatsub_id(message: Message, state: FSMContext):
    await state.clear()
    chat_and_sub_id = await ST.get_strip_sub_id(message.text)
    db_admins_cid_redis.hset(message.from_user.id, chat_and_sub_id[0], "") # Сохраняем в бд 0 в формате admin_id -> chat_id
    db_analysts_cid_redis.hset(chat_and_sub_id[0], chat_and_sub_id[1], f"{chat_and_sub_id[2]}:{chat_and_sub_id[3]}:{chat_and_sub_id[4]}:{chat_and_sub_id[5]}")
    await message.answer(f"👌 Добавлен/Перезаписан пользователь: {chat_and_sub_id[0]}")
