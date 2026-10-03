import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio
from backend.logic import  save_user_cv, get_new_vac,get_last3, get_pg
import selectors
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message,CallbackQuery
from aiogram import F, Router
from backend.bot.key_btns import cmd_start,router,StartCV,pagination_keyboard
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from backend.bot.hendlers import profile_cv
from APIs.main_apis import get_tj
import time
import httpx
import math

load_dotenv()
loop = lambda:asyncio.SelectorEventLoop(selectors.SelectSelector())
TOKEN = os.getenv("TG_API_TOKEN")
if TOKEN is None:
    raise ValueError("NOTFOUND TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()






        
        

@router.callback_query(F.data.startswith("today:page:"))
async def paginate(callback: CallbackQuery):
    page_number = int(callback.data.split(":")[2])
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/jobs")
    result = response.json()
    total_pages = math.ceil(len(result) / 5)
    if page_number < 1 or page_number > total_pages:
        await callback.answer("Page does not exist")
        return
    page =await get_pg(result, page_number)
    for i, vac in enumerate(page):
        if i == len(page) - 1:
            await callback.message.answer(
                vac,
                reply_markup=pagination_keyboard(
                    page_number,
                    total_pages,
                    "today"
                )
            )
        else:
            await callback.message.answer(vac)
    await callback.answer()


@router.message(F.text == "Today Vacancy")
async def tdvac(message : Message):
    async with httpx.AsyncClient() as cl:
        resp = await cl.get("http://127.0.0.1:8000/jobs")
    result = resp.json()
    total_pages = math.ceil(len(result)/5)
    page_num = 1
    page = await get_pg(result, page_num)
    for i,vac in enumerate(page):
        if i == len(page) -1:
            await message.answer(vac, reply_markup=pagination_keyboard(page_num, total_pages,"today"))
        else:
            await message.answer(vac)


@router.callback_query(F.data.startswith("acc:page:"))
async def paginates(callback: CallbackQuery):
    page_number = int(callback.data.split(":")[2])
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/acjobs")
    result = response.json()
    total_pages = math.ceil(len(result) / 5)
    if page_number < 1 or page_number > total_pages:
        await callback.answer("Page does not exist")
        return
    page =await get_pg(result, page_number)
    for i, vac in enumerate(page):
        if i == len(page) - 1:
            await callback.message.answer(
                vac,
                reply_markup=pagination_keyboard(
                    page_number,
                    total_pages,
                    "acc"
                )
            )
        else:
            await callback.message.answer(vac)
    await callback.answer()
@router.message(F.text == "Accepted Vacancies")
async def acvac(message : Message):
    async with httpx.AsyncClient() as cl:
        resp = await cl.get("http://127.0.0.1:8000/acjobs")
    result = resp.json()
    total_pages = math.ceil(len(result)/5)
    page_num = 1
    page = await get_pg(result, page_num)
    for i,vac in enumerate(page):
        if i == len(page) -1:
            await message.answer(vac, reply_markup=pagination_keyboard(page_num, total_pages,"acc"))
        else:
            await message.answer(vac)





@router.callback_query(F.data == "last_3_days_vac")
async def get_l3_d(callbac:CallbackQuery):
    result = await get_last3()
    for i in range(0,len(result), 10):
        part = "\n\n".join(result[i:i+10])
        assert callbac.message is not None
        await callbac.message.answer(part)
    await callbac.answer()


@router.callback_query(F.data == "get_today")
async def get_td(callback: CallbackQuery):
    result = await get_new_vac()
    for i in range(0, len(result),10):
        part = "\n""\n".join(result[i:i + 10])
        assert callback.message is not None
        await callback.message.answer(part)
    await callback.answer()




async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
