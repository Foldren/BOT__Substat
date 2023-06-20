from aiogram.fsm.state import State, StatesGroup


class StepsAddUser(StatesGroup):
    writing_chatsub_id = State()

