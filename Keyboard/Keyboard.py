import lexicon
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_menu_buttons = ([KeyboardButton(text=lexicon.main_menu_keys[i]) for i in range(len(lexicon.main_menu_keys))])
secondary_menu_buttons = ([KeyboardButton(text=lexicon.cases_keys[i]) for i in range(len(lexicon.cases_keys))])

kb_main_builder = ReplyKeyboardBuilder()
kb_secondary_builder = ReplyKeyboardBuilder()

kb_main_builder.row(*main_menu_buttons)
kb_secondary_builder.row(*secondary_menu_buttons)

kb_main_builder.adjust(3)
kb_secondary_builder.adjust(2)

kb_main_markup = kb_main_builder.as_markup(resize_keyboard=True)
kb_secondary_markup = kb_secondary_builder.as_markup(resize_keyboard=True)

