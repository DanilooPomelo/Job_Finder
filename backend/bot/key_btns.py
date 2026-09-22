from aiogram import Router,types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


router = Router()
def keyboardall():
    reply_kb = ReplyKeyboardBuilder()
    reply_kb.add(
        types.KeyboardButton(text="Today Vacancy"),
        types.KeyboardButton(text="New vacancies"),

)
    reply_kb.adjust(2)
    
    
    return reply_kb.as_markup(resize_keyboard=True)

def pagination_keyboard(page:int, total_pages:int):
    kb = InlineKeyboardBuilder()
    if page > 1:
        kb.button(
            text="⬅️ Back",
            callback_data=f"page:{page - 1}"
        )

    
    if page < total_pages:
        kb.button(
            text="Next ➡️",
            callback_data=f"page:{page + 1}"
        )

    kb.adjust(2)

    return kb.as_markup()


next_back = InlineKeyboardMarkup(

    inline_keyboard=[
        [
            InlineKeyboardButton(text="Next",callback_data="next"),
         ]
    ]

)

#inline_kb = InlineKeyboardMarkup(
    #inline_keyboard=[
       # [
        #    InlineKeyboardButton(
        #        text="Start CV for u",
        #        callback_data="btnclick"
        #    ),
        #    InlineKeyboardButton(
        #        text="get remote Vacancy",
        #        callback_data="remotevacancy"
        #    ),
        #    InlineKeyboardButton(
        #        text="Today Vacancy",
        #        callback_data="get_today"
        #    ),
        #    InlineKeyboardButton(
        #        text="Get last 3-dayd",
        #        callback_data="last_3_days_vac"
        #    )
#
#        ]
#    ]
#)


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
        reply_markup=keyboardall()
    )
