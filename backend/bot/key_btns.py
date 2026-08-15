from aiogram import Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


router = Router()

inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Start CV for u",
                callback_data="btnclick"
            ),
            InlineKeyboardButton(
                text="get remote Vacancy",
                callback_data="remotevacancy"
            ),
            InlineKeyboardButton(
                text="Today Vacancy",
                callback_data="get_today"
            ),
            InlineKeyboardButton(
                text="Get last 3-dayd",
                callback_data="last_3_days_vac"
            )

        ]
    ]
)


class StartCV(StatesGroup):
    profession = State()
    skills = State()
    frameworks = State()
    sqls = State()
    level = State()

    


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Welcome To Job AI Searcher Bot",
        reply_markup=inline_kb
    )
