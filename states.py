from aiogram.fsm.state import State, StatesGroup


class AskFlow(StatesGroup):
    waiting_name = State()
    asking = State()
