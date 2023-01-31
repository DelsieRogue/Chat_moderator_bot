from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from keyboards import get_inline_buttons, get_menu
from utils import dp, bot


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await get_menu(message)


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


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
