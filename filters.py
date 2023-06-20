from aiogram.filters import BaseFilter
from aiogram.types import Message
from tools import SubStatTools as ST
from config import db_admins_cid_redis, db_analysts_cid_redis
from aiogram.fsm.context import FSMContext


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in await ST.get_list_admins()


class IsAnalystsFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in await ST.get_list_analysts()


class CheckChatIdFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        chat_and_sub_id = message.text.split("\n")
        if int(chat_and_sub_id[0]) not in await ST.get_list_admins(): # Проверяем есть ли id в списке админов
            return True
        else:
            await message.answer(f"Нельзя добавлять chat_id админа, введите другое значение 🙅‍♂")
            return False


class IsAddUserFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return message.text != "Забрать доступ"


class CheckCountChatIdFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        chat_ids_list = await ST.get_list_users_keys(db_admins_cid_redis.hgetall(message.from_user.id))
        if chat_ids_list:
            return True
        else:
            await message.answer(text="Вы пока не добавили ниодного пользователя 🤷‍♂")
            return False


class CheckCountSubIdFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        chat_ids_list = await ST.get_list_users_keys(db_analysts_cid_redis.hgetall(message.from_user.id), admin=False)
        if chat_ids_list:
            return True
        else:
            await message.answer(text="Пока что для вас не расшарили ниодного sub_id 🤷‍♂")
            return False
