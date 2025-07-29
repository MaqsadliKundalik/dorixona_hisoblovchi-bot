from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

admin_menu = ReplyKeyboardBuilder()
admin_menu.button(text="Dorilar ro'yhati")
admin_menu.button(text="Dori qo'shish")
admin_menu.button(text="Dori o'chirish")
admin_menu.button(text="Narxini o'zgartirish")
admin_menu.adjust(1, 2, 1)
admin_menu = admin_menu.as_markup(resize_keyboard=True)

cancel_btn = ReplyKeyboardBuilder().button(text="Bekor qilish").as_markup(resize_keyboard=True)

def get_drugs_lst_btn(drugs):
    markup = ReplyKeyboardBuilder()
    markup.button(text="Bekor qilish")
    for drug in drugs:
        markup.button(text=drug)
    markup.adjust(1, 2)
    return markup.as_markup(resize_keyboard=True)

hisobot_btn = ReplyKeyboardBuilder().button(text="Spetsifikatsiya olish").as_markup(resize_keyboard=True)

confirm_btn = ReplyKeyboardBuilder().button(text="Ha").button(text="Yo'q").as_markup(resize_keyboard=True)
