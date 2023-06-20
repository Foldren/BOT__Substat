from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from states.state_remove_user import StepsRemoveUser
from aiogram import Router
from aiogram.filters import Text
from buttons import generate_cols_btns_keyboard
from config import db_admins_cid_redis, db_analysts_cid_redis
from filters import IsAdminFilter, CheckCountChatIdFilter
from tools import SubStatTools as ST

rt = Router()
rt.message.filter(IsAdminFilter())


@rt.message(Text(text="Забрать доступ"), CheckCountChatIdFilter())
async def get_list_chat_id(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(StepsRemoveUser.choosing_chat_id)
    chat_ids_list = await ST.get_list_users_keys(db_admins_cid_redis.hgetall(message.from_user.id))
    await message.answer(
        text="👉 Нажмите на chat_id пользователя, доступ анулируется ко всем сабам автоматически после нажатия❗",
        reply_markup=generate_cols_btns_keyboard(chat_ids_list, "chat_id_rm", 3))


@rt.callback_query(StepsRemoveUser.choosing_chat_id, Text(startswith="chat_id_rm"))
async def remove_chatsub_id(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    rm_chat_id = await ST.reformat_byte_to_str(callback.data.split(":")[1])
    db_admins_cid_redis.hdel(callback.from_user.id, rm_chat_id)
    db_analysts_cid_redis.delete(rm_chat_id)  # удаляем все сабы
    await callback.message.answer(f"🤛 Забрали доступ у пользователя: {rm_chat_id}")
