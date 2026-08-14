from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from backend.bot.key_btns import router , StartCV
from aiogram import F
from aiogram.types import Message, CallbackQuery
from backend.logic import save_user_cv

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