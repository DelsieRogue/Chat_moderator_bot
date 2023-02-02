from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

from keyboards import get_inline_buttons, get_menu, button_paid, button_to_pay
from scripts import set_role
from utils import dp, bot


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await get_menu(message)


# @dp.message_handler(commands=['add_user'])
# async def add_user(message: types.Message):
#     await bot.send_message(message.from_user.id, set_role(message, "USER"))


@dp.message_handler(Text("GODS"))
async def get_superadmins(message: types.Message):
    await bot.send_message(message.from_user.id, "Список королей",
                           reply_markup=await get_inline_buttons(["SUPER_ADMIN"]))


@dp.message_handler(Text("ADMINS"))
async def get_admins(message: types.Message):
    await bot.send_message(message.from_user.id, "Cписок админов", reply_markup=await get_inline_buttons(["ADMIN"]))


@dp.message_handler(Text("USERS"))
async def get_users(message: types.Message):
    await bot.send_message(message.from_user.id, "Список клиентов", reply_markup=await get_inline_buttons(["USER"]))


@dp.message_handler(Text("EX USERS"))
async def get_ex_users(message: types.Message):
    await bot.send_message(message.from_user.id, "Список бывших", reply_markup=await get_inline_buttons(["EX_USER"]))


@dp.callback_query_handler(text="buy_subscribe")
async def buy_subscribe(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, "Реквизиты", reply_markup=button_paid)
    await callback.answer("")


@dp.callback_query_handler(text="bought")
async def bought(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, "ваш запрос в обработке")

    button_buy_success = InlineKeyboardMarkup(row_width=4, resize_keyboard=True)\
        .add(InlineKeyboardButton(text="Деньги капнули", callback_data="buy_success" + str(callback.from_user.id)))\
        .add(InlineKeyboardButton(text="Денег нет сук(", callback_data="buy_failure" + str(callback.from_user.id)))

    await bot.send_message(478086330, "user = " + callback.from_user.username, reply_markup=button_buy_success)
    await callback.answer("")


@dp.callback_query_handler(lambda c: c.data.startswith('buy_success'))
async def buy_success(callback: types.CallbackQuery):
    user_id = int(callback.data.replace("buy_success", ""))
    set_role(user_id, "USER")
    await bot.send_message(user_id, "Это успех")
    await callback.answer("")


@dp.callback_query_handler(lambda c: c.data.startswith('buy_failure'))
async def buy_failure(callback: types.CallbackQuery):
    user_id = int(callback.data.replace("buy_failure", ""))
    await bot.send_message(user_id, "Плати пидор", reply_markup=button_paid)
    await callback.answer("")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
