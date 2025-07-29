from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from config import MAIN_ADMIN, ADMIN
from filters import IsMainAdmin, IsAdmin
from keyboards import admin_menu, hisobot_btn
from aiogram.fsm.context import FSMContext  

router = Router()

@router.message(IsMainAdmin(), Command("start"))
async def start_command_main_admin(message: Message):
    await message.answer(
        "Assalomu alaykum, Asosiy Admin! Xush kelibsiz!",
        reply_markup=admin_menu
    )

@router.message(IsAdmin(), Command("start"))
async def start_command_admin(message: Message):
    await message.answer(
        "Assalomu alaykum, Admin! Xush kelibsiz!"
    )

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        f"Assalomu alaykum! Xush kelibsiz!",
        reply_markup=hisobot_btn
    )

@router.message(IsMainAdmin(), F.text == "Bekor qilish")
async def f(message: Message, state:FSMContext):
    await message.answer("Jarayon bekor qilidni!", reply_markup=admin_menu)
    await state.clear()

@router.message(F.text == "Bekor qilish")
async def f(message: Message, state:FSMContext):
    await message.answer("Jarayon bekor qilidni!", reply_markup=hisobot_btn)
    await state.clear()