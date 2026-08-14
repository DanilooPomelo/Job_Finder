import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio
from backend.logic import get_remote, save_user_cv, get_new_vac, get_today_vac
import selectors
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message,CallbackQuery
from aiogram import F, Router
from backend.bot.key_btns import cmd_start,router,StartCV
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from backend.bot.hendlers import profile_cv

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






@router.callback_query(F.data == "get_today")
async def get_td(callback: CallbackQuery):
    result = await get_today_vac()
    for i in range(0, len(result),10):
        part = "\n""\n".join(result[i:i + 10])
        await callback.message.answer(part)
    await callback.answer()


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