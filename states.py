from aiogram.fsm.state import State, StatesGroup

class DrugState(StatesGroup):
    add_drug_name = State()
    add_drug_price = State()
    add_drug_date = State()
    add_drug_author = State()

    del_drug_name = State()
    
    edit_drug_name = State()
    edit_drug_price = State()

class HisobotState(StatesGroup):
    apteka = State()
    drug = State()
    quantity = State()
    confirm = State()