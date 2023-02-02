from aiogram import Bot, Dispatcher, types

import cnf
from scripts import get_role, set_role

bot = Bot(token=cnf.TOKEN)
dp = Dispatcher(bot)


# async def set_role(message: types.Message, to_role_name):
    # message.l
    # role = get_role(user_id)[0]
    # if role == "USER" or role == "NO_USER":
    #     return "У вас нет прав"
    # set_role(user_id, to_role_name)
    # return "Права обновлены"

