
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks.save_link import CategoryCB, SkipDescriptionCB, MakeDesiredActionCB


def categories_kb(categories: list):
    kb = InlineKeyboardBuilder()
    for name in categories:
        kb.button(text=name, callback_data=CategoryCB(category=name))

    kb.adjust(2)
    return kb.as_markup()


def skip_description_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Без описания", callback_data=SkipDescriptionCB(action="skip"))
    return kb.as_markup()


def actions_kb(actions: list):
    kb = InlineKeyboardBuilder()
    for name in actions:
        kb.button(text=name, callback_data=MakeDesiredActionCB(action=name))
    kb.adjust(1)
    return kb.as_markup()
