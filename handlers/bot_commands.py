__all__ = [
    "commands_for_bot"
]

from aiogram import types

bot_commands = (
    ("help", "Справка по боту"),
    ("start", "Регистрация нового пользователя"),
    ("status", "Вывод статуса пользователя"),
    ("register", "Регистрация в API Яндекс Диска"),
    ("token", "Проверка токена API Яндекс Диска"),
    ("add", "Добавить папку на Яндекс Диске в отслеживаемые"),
    ("delete", "Удалить папку из отслеживаемых"),
)

commands_for_bot = []
for cmd, descr in bot_commands:
    commands_for_bot.append(types.BotCommand(command=cmd, description=descr))
