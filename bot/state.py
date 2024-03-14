from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    menu = State()
    calendar = State()
    s_i = State()
    info = State()
    reklama = State()
