from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from utils import create_excel
from keyboards import cancel_btn, hisobot_btn, get_drugs_lst_btn, confirm_btn
from aiogram.fsm.context import FSMContext
from models.drug import Drug
from states import HisobotState
from config import MAIN_ADMIN, ADMIN

router = Router()

@router.message(F.text == "Spetsifikatsiya olish")
async def f(message: Message, state: FSMContext):
    await message.answer("Dorixona nomini kiriting.", reply_markup=cancel_btn)
    await state.set_state(HisobotState.apteka)
    
@router.message(HisobotState.apteka, F.text)
async def f(message: Message, state: FSMContext):
    if len(message.text) > 100: 
        await message.answer("Dorixona nomi juda uzun!")
        return
    await state.update_data(apteka=message.text)

    drugs = await Drug.all()
    drug_names = [d.name for d in drugs]
    await message.answer("Dorini tanlang.", reply_markup=get_drugs_lst_btn(drug_names))
    await state.set_state(HisobotState.drug)

@router.message(HisobotState.drug, F.text)
async def f(message: Message, state: FSMContext):
    drug_name = message.text
    drug = await Drug.get_or_none(name=drug_name)
    if not drug: 
        await message.answer("Dori topilmadi!", reply_markup=cancel_btn)
        return
    await state.update_data(drug=drug)
    await message.answer("Nechta dori oldingiz sonini kirting.", reply_markup=cancel_btn)
    await state.set_state(HisobotState.quantity)

@router.message(HisobotState.quantity, F.text)
async def f(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, son kiriting.")
        return
    quantity = int(message.text)
    data = await state.get_data()
    drug = data.get("drug")
    apteka = data.get("apteka")
    products = data.get("products", [])
    products.append({
        "name": drug.name,
        "quantity": quantity,
        "price": drug.price,
        "date": drug.date,
        "author": drug.author
    })
    await state.update_data(products=products)
    await message.answer("Yana dori kiritamizmi?", reply_markup=confirm_btn)
    await state.set_state(HisobotState.confirm)

@router.message(HisobotState.confirm, F.text)
async def f(message: Message, state: FSMContext):
    if message.text == "Ha":
        drugs = await Drug.all()
        drug_names = [d.name for d in drugs]
        await message.answer("Dorini tanlang.", reply_markup=get_drugs_lst_btn(drug_names))
        await state.set_state(HisobotState.drug)
    else:    
        data = await state.get_data()
        products = data.get("products")
        apteka = data.get("apteka")
        create_excel(products, apteka, "XASAN XUSAN FARM MCHJ", "hisobot.xlsx")

        await message.answer_document(FSInputFile("hisobot.xlsx"), caption=f"Hisobot {apteka} {message.date.date()}", reply_markup=hisobot_btn)
        await message.bot.send_document(ADMIN, FSInputFile("hisobot.xlsx"), caption=f"Hisobot {apteka} {message.date.date()}", reply_markup=hisobot_btn)