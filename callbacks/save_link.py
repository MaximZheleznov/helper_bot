from aiogram.filters.callback_data import CallbackData


class CategoryCB(CallbackData, prefix="cat"):
    category: str


class SkipDescriptionCB(CallbackData, prefix="desc"):
    action: str


class MakeDesiredActionCB(CallbackData, prefix="exist"):
    action: str
