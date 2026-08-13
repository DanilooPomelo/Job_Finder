import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio
from backend.logic import get_remote, save_user_cv
import selectors
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message,CallbackQuery
from aiogram import F, Router
from backend.bot.key_btns import cmd_start,router,StartCV
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


load_dotenv()
loop = lambda:asyncio.SelectorEventLoop(selectors.SelectSelector())
TOKEN = os.getenv("TG_API_TOKEN")
if TOKEN is None:
    raise ValueError("NOTFOUND TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()






@dp.message(Command("GET"))
async def get_remotes(messege):
    result = await get_remote()
    for i in range(0, len(result), 10):
        part = "\n""\n".join(result[i:i + 10])
        await messege.answer(part)


@router.callback_query(F.data == "btnclick")
async def start_btn_cv(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Your profession?")
    await state.set_state(StartCV.profession)

@router.message(StateFilter(StartCV.profession))
async def prof_name(messege: Message, state: FSMContext):
    await state.update_data(user_prof=messege.text)
    await messege.answer("What IT languages u Know?")
    await state.set_state(StartCV.skills)

@router.message(StateFilter(StartCV.skills))
async def frameworks_name(messege: Message, state: FSMContext):
    await state.update_data(user_skills=messege.text)
    await messege.answer("Whats FrameWorks u Know?")
    await state.set_state(StartCV.frameworks)

@router.message(StateFilter(StartCV.frameworks))
async def sqls_names(messege: Message, state: FSMContext):
    await state.update_data(user_frameworks=messege.text)
    await messege.answer("What sql db u Know?")
    await state.set_state(StartCV.sqls)

@router.message(StateFilter(StartCV.sqls))
async def level_names(messege: Message, state: FSMContext):
    await state.update_data(user_sqls=messege.text)
    await messege.answer("What level u have?")
    await state.set_state(StartCV.level)

@router.message(StateFilter(StartCV.level))
async def end_cv(messege:Message, state: FSMContext):
    await state.update_data(user_level=messege.text)
    use_cv = []
    user_data = await state.get_data()
    use_cv.append(user_data)
    await save_user_cv(user_data)
    await state.clear()


    result_cv = (
        "welldone"
        f"profession - {user_data.get("user_prof")}"
    )
    await messege.answer(result_cv)



@router.callback_query(F.data == "remotevacancy")
async def start_btn_rem(callback: CallbackQuery):
    result = await get_remote()
    for i in range(0, len(result), 10):
        part = "\n""\n".join(result[i:i + 10])
        await callback.message.answer(part)
    await callback.answer()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main(),loop_factory=loop)