from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from case_states.case_states import CaseStates
from keyboard.keyboards import categories_kb, actions_kb
from callbacks.save_link import CategoryCB, MakeDesiredActionCB
from shifts.shifts import get_current_working_shift
from filters.filters import ChatThreadFilter, UserFilter
import database.bot_data
import config
import lexicon


router = Router()


router.message.filter(ChatThreadFilter(config.theme_ids))
router.callback_query.filter(ChatThreadFilter(config.theme_ids))


@router.message(Command('fetch_data'))
async def fetch_bot_data(message: Message):
    data = database.bot_data.data.fetch_data(chat_id=str(message.chat.id))
    response = ''
    i = 1
    await message.delete()
    for key in data.keys():
        response += f"{key}\n"
        for k in data[key]:
            response += f"{i}. {k}\n"
            i += 1
        response += "\n"
    await message.answer(f"{'Вот текущий список кейсов:' if response else 'На текущий момент, список пуст😦'}\n\n{response}")


@router.message(Command('fetch_data_final'), UserFilter(config.admin_users))
async def fetch_bot_data_final(message: Message):
    await message.delete()
    data = database.bot_data.data.fetch_data_final(chat_id=str(message.chat.id))
    shift = get_current_working_shift()
    response = ''
    for key in data.keys():
        response += f"{key}\n"
        for k in data[key]:
            response += f"{k}\n"
        response += "\n"
    await message.answer(f"{f'Список кейсов для КП за: {shift[1]} {shift[2]}' if response else 'На текущий момент, список пуст😦'}\n\n{response}")


@router.message(Command('group_delete'), UserFilter(config.admin_users))
async def group_delete_handler(message: Message, state: FSMContext):
    await message.delete()
    await message.answer("Пришлите список кейсов для удаления")
    await state.set_state(CaseStates.waiting_for_deletion_list)


@router.message(CaseStates.waiting_for_deletion_list, UserFilter(config.admin_users))
async def remove_group(message: Message, state: FSMContext):
    case_links = message.text.split()
    response = ''
    await message.delete()
    for link in case_links:
        response += f"\n{database.bot_data.data.remove_data(link, chat_id=str(message.chat.id))}"
    await message.answer(response)
    await state.set_state(CaseStates.waiting_for_link)
    database.bot_data.data.save_data()


@router.message(Command('clean_data'), UserFilter(config.admin_users))
async def clean_bot_data(message: Message):
    await message.delete()
    await message.answer(database.bot_data.data.clean_data(chat_id=str(message.chat.id)))
    database.bot_data.data.save_data()


@router.message(Command('echo_chat_id'))
async def echo_chat_id(message: Message):
    await message.answer(f"ID темы: {message.message_thread_id}\n ID чата: {message.chat.id}")


@router.message(F.text.startswith("https://t.me"))
async def receive_link(message: Message, state: FSMContext):
    link = message.text.split(maxsplit=1)[0]
    description = ''
    await message.delete()
    if len(message.text.split(maxsplit=1)) > 1:
        description = message.text.split(maxsplit=1)[1]
    if database.bot_data.data.is_in_dict(link=link, chat_id=str(message.chat.id)):
        response = f"{database.bot_data.data.data[str(message.chat.id)][link][0]} {database.bot_data.data.data[str(message.chat.id)][link][1]}"
        await message.answer(f"Такая ссылка уже сохранена:\n{link} {response}\n\nХотите внести изменения в кейс?", reply_markup=actions_kb(lexicon.main_menu_keys))
        await state.set_state(CaseStates.waiting_for_action)
        await state.update_data(link=link, description=description)
        return
    await state.update_data(link=link, description=description)
    await message.answer("Выберите категорию", reply_markup=categories_kb(lexicon.cases_keys))
    await state.set_state(CaseStates.waiting_for_category)


@router.callback_query(CaseStates.waiting_for_action, MakeDesiredActionCB.filter())
async def choose_action(callback: CallbackQuery, callback_data: MakeDesiredActionCB, state: FSMContext):
    action = callback_data.action
    if action == "Изменить категорию":
        await callback.message.edit_text("Выберите новую категорию:", reply_markup=categories_kb(lexicon.cases_keys))
        await state.set_state(CaseStates.waiting_for_new_category)
    elif action == "Удалить кейс":
        data = await state.get_data()
        await callback.message.edit_text(database.bot_data.data.remove_data(case_link=data["link"], chat_id=str(callback.message.chat.id)))
        database.bot_data.data.save_data()
        await state.set_state(CaseStates.waiting_for_link)
    elif action == "Назад":
        await callback.message.edit_text("Вернулись в главное меню.\nОжидаю ссылку для продолжения работы.")
        await state.set_state(CaseStates.waiting_for_link)
    await callback.answer()


@router.callback_query(CaseStates.waiting_for_new_category, CategoryCB.filter())
async def set_new_category(callback: CallbackQuery, callback_data: CategoryCB, state: FSMContext):
    await state.update_data(category=callback_data.category)
    data = await state.get_data()
    link = data["link"]
    category = data["category"]
    description = data["description"]
    await callback.message.edit_text(database.bot_data.data.change_data(new_data=[link, category, description], chat_id=str(callback.message.chat.id)))
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
    await callback.message.edit_text(database.bot_data.data.add_data(input_data=[link, category, description], chat_id=str(callback.message.chat.id)))
    await state.set_state(CaseStates.waiting_for_link)
    await callback.answer()
    database.bot_data.data.save_data()
