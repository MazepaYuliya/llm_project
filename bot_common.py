"Общие команды бота"
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section
)

# from constants import PULSE_USER_LINK
from ml_functions import find_by_name, find_by_question


router = Router()


class EntityAction(StatesGroup):
    """Класс состояний запросов"""
    find_entity = State()
    new_question = State()
    
    
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Хэндлер для команды start.
    Приветствие пользователя
    """
    await message.reply(
        "Здравствуйте!\n\n"
        "Я бот для поиска информации о болезнях.\n"
        "Для просмотра моих текущих возможностей выберите команду /help",
        parse_mode=ParseMode.HTML
    )


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """
    Хэндлер для команды help.
    Список доступных команд
    """
    content = as_list(
        as_marked_section(
            Bold("Список доступных команд:"),
            "/find_entity - выполнить поиск по названию болезни",
            "/new_question - задать вопрос про болезнь",
            marker="✔️ ",
        ),
        sep="\n\n",
    )
    await message.reply(**content.as_kwargs())


@router.message(StateFilter(None), Command("find_entity"))
async def cmd_find_entity(message: types.Message, state: FSMContext):
    """
    Хэндлер для команды find_entity.
    Поиск информации по названию болезни
    """
    await message.reply(
        "Введите название болезни:",
    )
    current_state = getattr(EntityAction, message.text.replace('/', ''))
    await state.set_state(current_state)
    
    
@router.message(EntityAction.find_entity)
async def get_entity_info(message: types.Message, state: FSMContext):
    """
    Хэндлер для команды find_entity.
    Поиск информации по названию болезни
    """
    entity_name = message.text
    await state.clear()
    
    found_info = find_by_name(entity_name)
    
    if not found_info:
        text = 'К сожалению, по данной болезни не удалось ничего найти'
    else:
        text = f'<b>Найденная информация:</b>\n\n{found_info}'

    await message.answer(
        text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )


@router.message(StateFilter(None), Command("new_question"))
async def cmd_new_question(message: types.Message, state: FSMContext):
    """
    Хэндлер для команды new_question.
    Поиск ответа на вопрос пользователя
    """
    await message.reply(
        "Введите вопрос:",
    )
    current_state = getattr(EntityAction, message.text.replace('/', ''))
    await state.set_state(current_state)
    

@router.message(EntityAction.new_question)
async def get_question_info(message: types.Message, state: FSMContext):
    """
    Хэндлер для команды new_question.
    Поиск ответа на вопрос пользователя
    """
    question = message.text
    await state.clear()
    
    found_info = find_by_question(question)
    
    if not found_info:
        text = 'К сожалению, по данному вопросу не удалось ничего найти'
    else:
        text = f'<b>Найденная информация:</b>\n\n{found_info}'

    await message.answer(
        text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )
