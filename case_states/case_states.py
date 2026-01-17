from aiogram.fsm.state import State, StatesGroup


class CaseStates(StatesGroup):
    waiting_for_link = State()
    waiting_for_category = State()
    waiting_for_description = State()
    waiting_for_action = State()
    waiting_for_new_category = State()
    waiting_for_new_description = State()


