from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from scripts import get_users_from_db, get_role, add_user_to_table_users
from utils import bot

kb = [
    KeyboardButton(text="NO USERS"),
    KeyboardButton(text="USERS"),
    KeyboardButton(text="ADMINS"),
    KeyboardButton(text="GODS")
]

admins_button = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True).add(*kb)

kb2 = [
    KeyboardButton(text="1"),
    KeyboardButton(text="2"),
    KeyboardButton(text="3"),
    KeyboardButton(text="4")
]

users_buttons = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True).add(*kb2)

buttons_pay = {
    "Оплатить": InlineKeyboardButton(text="Оплатить", callback_data="buy_subscribe"),
    "Подтвердить оплату": InlineKeyboardButton(text="Подтверждаю оплату", callback_data="bought"),
}

button_to_pay = InlineKeyboardMarkup(row_width=4, resize_keyboard=True).add(buttons_pay.get("Оплатить"))
button_paid = InlineKeyboardMarkup(row_width=4, resize_keyboard=True).add(buttons_pay.get("Подтвердить оплату"))




async def get_menu(message: types.Message):
    role = get_role(message.from_user.id)
    if not role:
        add_user_to_table_users(message.from_user.id, message.from_user.username, "NO_USER",
                                message.from_user.first_name,
                                message.from_user.last_name)
    elif role[0] == "SUPER_ADMIN" or role[0] == "ADMIN":
        return await bot.send_message(chat_id=message.chat.id, text="commands", reply_markup=admins_button)

    elif role[0] == "USER":
        return await bot.send_message(chat_id=message.chat.id, text="commands", reply_markup=users_buttons)

    return await bot.send_message(chat_id=message.chat.id, text="Купить подписку",
                                  reply_markup=button_to_pay)


async def get_inline_buttons(roles):
    user_list = get_users_from_db(roles)
    inline_markup = InlineKeyboardMarkup(row_width=2)
    for user in user_list:
        inline_markup.add(InlineKeyboardButton(user[1] if user[1] else "FOREVER", callback_data=user[0]),
                          InlineKeyboardButton(user[0], url="https://t.me/" + user[0]))
    return inline_markup
