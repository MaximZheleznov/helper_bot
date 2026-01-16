from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
import Keyboard.Keyboard

router = Router()


@router.message(Command(commands='start'))
async def start(message: Message):
    await message.answer('Выберите категорию:', reply_markup=Keyboard.Keyboard.kb_main_markup)



