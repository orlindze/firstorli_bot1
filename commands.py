# import logging
# from aiogram.types import BotCommand

# logger = logging.getLogger(__name__)

# async def set_commands(bot):
#     commands = [
#         BotCommand(command="start", description="Запуск бота"),
#         BotCommand(command="help", description="Помощь"),
#         BotCommand(command="add", description="Добавить бойца"),
#         BotCommand(command="list", description="Список бойцов"),
#         BotCommand(command="delete", description="Удалить бойца"),
#         BotCommand(command="fight", description="Начать бой 50/50 между бойцами")
#     ]
#     await bot.set_my_commands(commands)

import logging
from aiogram.types import BotCommand

logger = logging.getLogger(__name__)

async def set_commands(bot):
    commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="help", description="Допомога"),
        BotCommand(command="add", description="Додати бійця"),
        BotCommand(command="list", description="Список бійців"),
        BotCommand(command="delete", description="Видалити бійця"),
        BotCommand(command="fight", description="Почати бій 50/50 між бійцями")
    ]
    await bot.set_my_commands(commands)