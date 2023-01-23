from aiogram.types import Message
from bot import bot, dp, rm, log


async def handle(message: Message):
    if rm.is_vacancy(message.text):
        result, checklist = rm.check(message.text)
        log.info(f'Вакансия от {message.from_user.username} \n"{message.text[:200]}..."\n\n'
                 f'Результат проверки: {checklist}')
        if result:
            pass
        else:
            body = ['Похоже, что у оформление вашей вакансии'
                    ' не соответствует правилам.\n'
                    'Ссылка на правила — https://t.me/python_vacancy/66\n'
                    'Проверьте по контрольному листу:\n\n']
            for item in checklist:
                body.append(f'{item[0]:<10}{"—":^10}{item[1]} \n')  # change in rules.RuleManager.check() - True = OK, False = X
            text = ''.join(body)
            await message.reply(text)


def register_user(d: dp):
    d.register_message_handler(handle)