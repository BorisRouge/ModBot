from aiogram.types import Message
from bot import bot, rm, log, config


async def handle(message: Message):
    """Основной обработчик сообщений бота.
       Проверяет сообщение на тег #вакансия и соответствие правилам,
       определенным в rules.py. Сообщает отправителю вакансии,
       по каким пунктам не проходит несоответствие."""
    try:
        if rm.is_vacancy(message.text):
            # Основная проверка через контроллер правил.
            result, checklist = rm.check(message.text)
            log.info(f'Вакансия от {message.from_user.username} '
                     f'\n"{message.text[:200]}..."\n\n'
                     f'Результат проверки: {checklist}')

            if not result:
                body = ['\nПохоже, что оформление вашей вакансии'
                        ' не соответствует правилам.\n'                    
                        'Проверьте по контрольному листу:`\n\n']
                # Форматирование ответа.
                for item in checklist:
                    n = len(item[0])
                    n = 20 if n > 20 else n
                    line = item[0][:20] + "—   ".rjust(25 - n) + item[1] + "\n"
                    body.append(line)
                body.append('`')
                body.append('\n*Ссылка на правила — https://t.me/python_vacancy/66*')
                text = ''.join(body)
                await message.reply(text, parse_mode="Markdown")
    except Exception as e:
        log.error(f'Ошибка в работе бота: \n {e}')
        await bot.send_message(config.telegram.admin,
                         f'Ошибка в работе бота: \n {e}')


def register_user(dp):
    dp.register_message_handler(handle)