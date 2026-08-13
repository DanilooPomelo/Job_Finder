import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio
from main import get_remote
import selectors
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
loop = lambda:asyncio.SelectorEventLoop(selectors.SelectSelector())
TOKEN = os.getenv("TG_API_TOKEN")
if TOKEN is None:
    raise ValueError("NOTFOUND TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_ha(messege):
    await messege.answer("ХАЮШКИ ДУРАЧОК")
@dp.message(Command("GET"))
async def get_remotes(messege):
    result = await get_remote()
    for i in range(0, len(result), 10):
        part = "\n""\n".join(result[i:i + 10])
        await messege.answer(part)

async def main():
    await dp.start_polling(bot)

asyncio.run(main(),loop_factory=loop)