from aiogram import F, Router
from aiogram.types import Message
import Data.bot_data
import Keyboard.Keyboard
import lexicon

router = Router()


@router.message(F.text.in_(Data.bot_data.data.data.keys()))
async def check_link(message: Message):
    link = message.text
    if message.text in Data.bot_data.data.data.keys():
        await message.answer("Кейс был ранее добавлен, выберите дальнейшее действие:", reply_markup=Keyboard.Keyboard.kb_main_markup)

    @router.message((F.text == 'Изменить категорию') or (F.text == 'Удалить кейс'))
    async def change_category(message: Message):
            category = message.text
            if category == 'Удалить кейс':
                Data.bot_data.data.remove_data(link)
                return
            await message.answer("Введите описание:")

            @router.message(F.text)
            async def change_data(message: Message):
                await message.answer(text=Data.bot_data.data.change_data([link, category, message.text]))


@router.message(F.text.contains("t.me"))
async def add_link(message: Message):
    link = message.text
    await message.answer(text="Выберите категорию:", reply_markup=Keyboard.Keyboard.kb_secondary_markup)

    @router.message(F.text.in_(lexicon.cases_keys))
    async def add_description(message: Message):
        category = message.text
        await message.answer("Введите описание кейса")

        @router.message(F.text)
        async def add_data(message: Message):
            Data.bot_data.data.add_data([link, category, message.text])
            await message.answer(text='Кейс добавлен!')





