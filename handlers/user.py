from aiogram.types import Message
from bot import bot, dp


async def handle(message:Message):

    for rule in rules:
        if rule.markers not in message.text:
            rule.triggered()
