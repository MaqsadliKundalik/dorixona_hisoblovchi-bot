from aiogram import Router, F
from aiogram.types import Message
from filters import IsMainAdmin, IsAdmin
from aiogram.fsm.context import FSMContext
from models.drug import Drug
from states import DrugState
from keyboards import cancel_btn, admin_menu, get_drugs_lst_btn

router = Router()

@router.message(IsMainAdmin(), F.text == "Dori qo'shish")
async def f(message: Message, state: FSMContext):
    await message.answer("Dori qo'shish uchun dori nomini yuboring:", reply_markup=cancel_btn)
    await state.set_state(DrugState.add_drug_name)

@router.message(DrugState.add_drug_name)
async def f(message: Message, state: FSMContext):
    drug_name = message.text
    if len(drug_name) > 30:
        await message.answer("Dori nomi 30 ta belgidan oshmasligi kerak.", reply_markup=cancel_btn)
        return
    await state.update_data(name=drug_name)
    await message.answer("Dori narxini kriting.", reply_markup=cancel_btn)
    await state.set_state(DrugState.add_drug_price)

@router.message(DrugState.add_drug_price)
async def f(message: Message, state: FSMContext):
    drug_price = int(message.text)
    await state.update_data(price=drug_price)
    await message.answer("Dorining amal qilish muddatini kiriting.", reply_markup=cancel_btn)
    await state.set_state(DrugState.add_drug_date)

@router.message(DrugState.add_drug_date, F.text)
async def f(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Dori ishlab chiqaruvchisini kirting.", reply_markup=cancel_btn)
    await state.set_state(DrugState.add_drug_author)

@router.message(DrugState.add_drug_author, F.text)
async def f(message: Message, state: FSMContext):
    state_data = await state.get_data()
    name = state_data.get("name")
    price = state_data.get("price")
    date = state_data.get("date")
    author = message.text
    await Drug.create(name=name, price=price, date=date, author=author)
    await message.answer("Dori muvaffaqiyatli qo'shildi.", reply_markup=admin_menu)
    await state.clear()

@router.message(IsMainAdmin(), F.text == "Dori o'chirish")
async def f(message:Message, state: FSMContext):
    drugs = await Drug.all()
    drug_names = [d.name for d in drugs]
    markup = get_drugs_lst_btn(drug_names)
    await message.answer("Dorini tanlang.", reply_markup=markup)
    await state.set_state(DrugState.del_drug_name)

@router.message(DrugState.del_drug_name, F.text)
async def f(message: Message, state: FSMContext):
    drug_name = message.text
    drug = await Drug.get_or_none(name=drug_name)
    if drug is None:
        await message.answer("Bunday dori topilmadi!")
        return
    
    await drug.delete()
    await message.answer("Droi muvaffaqoyatli o'chirildi!", reply_markup=admin_menu)
    await state.clear()

@router.message(F.text == "Narxini o'zgartirish")
async def f(message: Message, state: FSMContext):
    drugs = await Drug.all()
    drug_names = [d.name for d in drugs]
    markup = get_drugs_lst_btn(drug_names)
    await message.answer("Dorini tanlang.", reply_markup=markup)
    await state.set_state(DrugState.edit_drug_name)

@router.message(DrugState.edit_drug_name, F.text)
async def f(message: Message, state: FSMContext):
    drug_name = message.text
    drug = await Drug.get_or_none(name=drug_name)
    if not drug: 
        await message.answer("Dori topilmadi!", reply_markup=cancel_btn)
        return
    await state.update_data(drug=drug)
    await message.answer("Dorining yangi narxini kiriting.", reply_markup=cancel_btn)
    await state.set_state(DrugState.edit_drug_price)

@router.message(DrugState.edit_drug_price, F.text)
async def f(message: Message, state: FSMContext):
    state_data = await state.get_data()
    drug = state_data.get("drug")
    drug.price = int(message.text)
    await drug.save()
    await message.answer("Dori narxi o'zgartirildi!", reply_markup=admin_menu)
    await state.clear()

@router.message(IsMainAdmin(), F.text == "Dorilar ro'yhati")
async def f(message: Message, state: FSMContext):
    drugs = await Drug.all()
    if not drugs: 
        await message.answer("Droilar mavjud emas!")
        return
    text = "Dorilar ro'yhati:\n\n"
    for drug in drugs:
        text += f"{drug.name} - {drug.price:,} UZS"
    await message.answer(text=text)