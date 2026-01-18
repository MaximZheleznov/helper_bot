from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from datetime import datetime, timedelta
import config
from case_states.case_states import CaseStates
from keyboard.keyboards import categories_kb, actions_kb
from callbacks.save_link import CategoryCB, MakeDesiredActionCB
import database.bot_data
import lexicon


router = Router()


router.message.filter(F.message_thread_id == config.theme_id)
git router.callback_query.filter(F.message.message_thread_id == config.theme_id)


@router.message(Command("start"))
async def start_save(message: Message, state: FSMContext):
    await state.set_state(CaseStates.waiting_for_link)
    await message.answer("Привет!👋\nДавайте начнём!\nПришлите ссылку для сохранения!💾")


@router.message(Command('fetch_data'))
async def fetch_bot_data(message: Message):
    data = database.bot_data.data.fetch_data()
    response = ''
    for key in data.keys():
        response += f"{key}\n"
        for k in data[key]:
            response += f"{k}\n"
        response += "\n"
    await message.answer(f"{'Вот текущий список кейсов:' if response else 'На текущий момент, список пуст😦'}\n\n{response}")


@router.message(Command('fetch_data_final'))
async def fetch_bot_data_final(message: Message):
    if message.from_user.id in config.admin_users:
        date = datetime.utcnow()
        yesterday = datetime.today() - timedelta(days=1)
        yesterday = yesterday.strftime("%d.%m.%y")
        shifts = config.shifts
        if shifts[0][0] < date.hour <= shifts[0][1]:
            shift = shifts[0][2]
            date = date.strftime("%d.%m.%y")
        elif shifts[1][0] < date.hour <= shifts[1][1]:
            shift = shifts[1][2]
            date = date.strftime("%d.%m.%y")
        else:
            shift = shifts[2][2]
            date = yesterday
        data = database.bot_data.data.fetch_data_final()
        response = ''
        for key in data.keys():
            response += f"{key}\n"
            for k in data[key]:
                response += f"{k}\n"
        await message.answer(f"{f'Список кейсов для КП за: {shift} {date}' if response else 'На текущий момент, список пуст😦'}\n\n{response}")


@router.message(Command('group_delete'))
async def group_delete_handler(message: Message, state: FSMContext):
    if message.from_user.id in config.admin_users:
        await message.answer("Пришлите список кейсов для удаления")
        await state.set_state(CaseStates.waiting_for_deletion_list)


@router.message(CaseStates.waiting_for_deletion_list)
async def remove_group(message: Message, state: FSMContext):
    if message.from_user.id in config.admin_users:
        case_links = message.text.split()
        response = ''
        for link in case_links:
            response += f"\n{link}: {database.bot_data.data.remove_data(link)}"
        await message.answer(response)
        await state.set_state(CaseStates.waiting_for_link)
        database.bot_data.data.save_data()


@router.message(Command('clean_data'))
async def clean_bot_data(message: Message):
    if message.from_user.id in config.admin_users:
        await message.answer(database.bot_data.data.clean_data())
        database.bot_data.data.save_data()


@router.message(Command('echo_chat_id'))
async def echo_chat_id(message: Message):
    await message.answer(str(message.message_thread_id))


@router.message(CaseStates.waiting_for_link, F.text.startswith("https://t.me"))
async def receive_link(message: Message, state: FSMContext):
    link = message.text.split(maxsplit=1)[0]
    description = ''
    if len(message.text.split(maxsplit=1)) > 1:
        description = message.text.split(maxsplit=1)[1]
    if database.bot_data.data.is_in_dict(link):
        response = f"{database.bot_data.data.data[link][0]} {database.bot_data.data.data[link][1]}"
        await message.answer(f"Такая ссылка уже сохранена:\n{link} {response}\n\nХотите внести изменения в кейс?", reply_markup=actions_kb(lexicon.main_menu_keys))
        await state.set_state(CaseStates.waiting_for_action)
        await state.update_data(link=link, description=description)
        return
    await state.update_data(link=link, description=description)
    await message.answer("Выбери категорию", reply_markup=categories_kb(lexicon.cases_keys))
    await state.set_state(CaseStates.waiting_for_category)


@router.callback_query(CaseStates.waiting_for_action, MakeDesiredActionCB.filter())
async def choose_action(callback: CallbackQuery, callback_data: MakeDesiredActionCB, state: FSMContext):
    action = callback_data.action
    if action == "Изменить категорию":
        await callback.message.edit_text("Выберите новую категорию:", reply_markup=categories_kb(lexicon.cases_keys))
        await state.set_state(CaseStates.waiting_for_new_category)
    elif action == "Удалить кейс":
        data = await state.get_data()
        await callback.message.edit_text(database.bot_data.data.remove_data(data["link"]))
        await state.set_state(CaseStates.waiting_for_link)
    elif action == "Назад":
        await callback.message.edit_text("Вернулись в главное меню.\nОжидаю ссылку для продолжения работы.")
        await state.set_state(CaseStates.waiting_for_link)


@router.callback_query(CaseStates.waiting_for_new_category, CategoryCB.filter())
async def set_new_category(callback: CallbackQuery, callback_data: CategoryCB, state: FSMContext):
    await state.update_data(category=callback_data.category)
    data = await state.get_data()
    link = data["link"]
    category = data["category"]
    description = data["description"]
    await callback.message.edit_text(database.bot_data.data.change_data([link, category, description]))
    await state.set_state(CaseStates.waiting_for_link)
    await callback.answer()
    database.bot_data.data.save_data()


@router.callback_query(CaseStates.waiting_for_category, CategoryCB.filter())
async def choose_category(callback: CallbackQuery, callback_data: CategoryCB, state: FSMContext):
    await state.update_data(category=callback_data.category)
    data = await state.get_data()
    link = data["link"]
    category = data["category"]
    description = data["description"]
    await callback.message.edit_text(database.bot_data.data.add_data([link, category, description]))
    await state.set_state(CaseStates.waiting_for_link)
    await callback.answer()
    database.bot_data.data.save_data()
