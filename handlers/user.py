from aiogram.types import Message
from bot import bot, dp, rm, log


async def handle(message: Message):
    log.info(message.text)
    if rm.is_vacancy(message.text):
        result = rm.check(message.text)
        log.info(result)
        if result[0]:
            pass
        else:
            await message.reply(
                f'you have fucked up with the following:\n' # TODO: форматнуть в список
                f'{result[1]}')


def register_user(d: dp):
    d.register_message_handler(handle)