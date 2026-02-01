from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class ChatThreadFilter(BaseFilter):
    def __init__(self, allowed: dict[str, int]):
        self.allowed = allowed

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        if isinstance(event, CallbackQuery):
            message = event.message
        else:
            message = event

        if not message:
            return False

        chat_id = message.chat.id
        thread_id = message.message_thread_id
        if not thread_id:
            thread_id = ""
        if str(chat_id) not in self.allowed.keys():
            return False
        return self.allowed[str(chat_id)] == thread_id


class UserFilter(BaseFilter):
    def __init__(self, allowed_users: set[int]):
        self.allowed_users = allowed_users

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return event.from_user.id in self.allowed_users
