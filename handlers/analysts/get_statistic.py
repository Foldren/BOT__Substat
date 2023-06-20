from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from states.state_get_stat_sub_id import StepsGetStatistic
from aiogram import Router
from aiogram.filters import Text
from buttons import generate_cols_btns_keyboard
from config import db_analysts_cid_redis
from filters import IsAnalystsFilter, CheckCountSubIdFilter
from tools import SubStatTools as ST

rt = Router()
rt.message.filter(IsAnalystsFilter())


@rt.message(Text(startswith="Cтатистика за"), CheckCountSubIdFilter())
async def get_list_sub_id(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(StepsGetStatistic.choosing_sub_id)
    sub_ids = db_analysts_cid_redis.hgetall(message.from_user.id)
    list_sub_ids = await ST().convert_dict_bytes_to_list_str(sub_ids, "SUB", "TZ")
    range_stats = 'quarter' if ("неделю" in message.text) else ('month' if ("месяц" in message.text) else 'day')
    await message.answer(
        text="👉 Нажмите на нужный номер sub_id, по включенным в него sub_id будет выведена статистика❗",
        reply_markup=generate_cols_btns_keyboard(list_sub_ids, f"sub_id_check|{range_stats}|", 1)
    )


@rt.callback_query(StepsGetStatistic.choosing_sub_id, Text(startswith="sub_id_check"))
async def answer_statistic_day(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    date_range = callback.data.split("|")[1]
    sub_number = await ST.reformat_byte_to_str(callback.data.split(":")[1][3:])
    sub_ids_params = await ST.reformat_byte_to_str(str(db_analysts_cid_redis.hget(callback.from_user.id, sub_number)))
    sub_ids = sub_ids_params.split(":")[0]
    partner_id = sub_ids_params.split(":")[1]
    timezone = sub_ids_params.split(":")[2]
    geo = sub_ids_params.split(":")[3]
    stats = await ST.parse_stats(geo, sub_number, await ST.get_list_sub_id(sub_ids), partner_id, date_range, timezone)
    await callback.message.answer(await ST.get_stats_msg_from_callback(callback.data, stats))
