from aiogram.fsm.state import State, StatesGroup


class StepsRemoveUser(StatesGroup):
    choosing_chat_id = State()