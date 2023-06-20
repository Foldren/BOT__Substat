from aiogram.fsm.state import State, StatesGroup


class StepsGetStatistic(StatesGroup):
    choosing_sub_id = State()