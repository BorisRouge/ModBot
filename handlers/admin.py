from aiogram.types import Message, InputFile
from bot import bot, config, dp


async def get_rules(message: Message):
    """Выгружает файл с правилами по команде администратора в его личку."""
    rules_file = InputFile('utils/rules.py')
    await bot.send_document(message.from_id, rules_file)


def register_admin(d: dp):
    d.register_message_handler(get_rules, user_id=config.telegram.admin, commands=["admin"], state='*')