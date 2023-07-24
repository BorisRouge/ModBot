import os
import asyncio
import logging as log
from aiogram.types import Message
from bot import bot, rm, config

ADMIN = os.getenv('ADMIN')
TIMEOUT = 30*60

# Блэклист временно живет в оперативной памяти.
blacklist = {}


async def handle(message: Message):
    """Основной обработчик сообщений бота.
       Проверяет сообщение на тег #вакансия и соответствие правилам,
       определенным в rules.py. Сообщает отправителю вакансии,
       по каким пунктам не проходит несоответствие."""

    try:
        print(message.entities)


        
        #  Если резюме -- пропускаем
        if rm.is_cv(message.text):
            return
        
        #  Проверяем тэг.
        is_vacancy = rm.is_vacancy(message.text)

        # Основная проверка через контроллер правил.
        result, checklist = rm.check(message.text, message)

        log.info(f'Сообщение от {message.from_user.username} '
                 f'\n"{message.text[:200]}..."\n\n'
                 f'Результат проверки: {checklist}'
                 f'\nДлина сообщения: {len(message.text)}')

        #  Уведомляем при несоответствии.
        if not result and is_vacancy:
            await notify_recruiter(message, checklist)
            await on_clock(message, checklist)

        #  Не похоже ли на вакансию без тега?
        elif rm.is_suspicious(checklist, message.text) and not is_vacancy:
            await notify_recruiter(message, checklist, is_vacancy)
            await on_clock(message, checklist)

        #  Убираем из черного списка, если есть.
        elif result and is_vacancy:
            await like(message)

    except Exception as e:
        log.error(f'Ошибка в работе бота: \n {e}')
        await bot.send_message(ADMIN, f'Ошибка в работе бота: \n {e}')


async def notify_recruiter(message: Message, checklist, tag=True):
    """Уведомляем рекрутера о недочетах.
    Предусмотрен отдельный сценарий, если без #вакансия."""
    body = [
        '\nПохоже, что оформление вашей вакансии'
        ' не соответствует правилам.\n'
        'Проверьте по контрольному листу:`\n\n'
    ]

    if not tag:
        checklist.insert(0, ('Тэг вакансии', False))

    # Форматирование ответа.
    for item in checklist:
        value = 'OK' if item[1] else 'X'
        n = len(item[0])
        n = 20 if n > 20 else n
        line = item[0][:20] + "—   ".rjust(25 - n) + value + "\n"
        body.append(line)
    print(body)
    body.append('`')
    body.append('\n*Ссылка на правила — https://t.me/python_vacancy/66*')
    text = ''.join(body)

    await message.reply(text, parse_mode="Markdown")
    log.info(
        f"Пользователь {message.from_user.full_name} уведомлен о недочетах.")


async def on_clock(message: Message, old_checklist):
    """Повторная проверка после замечания."""    
    await asyncio.sleep(TIMEOUT)

    result, checklist = rm.check(message.text)
    tag = rm.is_vacancy(message.text)
    # Если есть изменения, значит рекрутер пытался исправить.
    if tag and not result and old_checklist != checklist:
        await notify_recruiter(message, checklist)
        await on_clock(message, checklist)
        log.info(
            f"Рекрутер {message.from_user.full_name} отредактировал вакансию, "
            + "но она не соответствует правилам. Рекрутер уведомлен, " +
            "дано дополнительное время")

    elif not result or not tag:
        try:
            await message.delete()
            log.info(
                f"Рекрутер {message.from_user.full_name} не исправил вакансию, "
                + "вакансия удалена")
            await dislike(message)
        except Exception as e:
            log.error(f'Ошибка в работе бота: \n {e}')
            await bot.send_message(ADMIN, f'Ошибка в работе бота: \n {e}')

    elif result and rm.is_vacancy(message.text):
        await message.reply('Вакансия в порядке, спасибо!')
        log.info(f"Рекрутер {message.from_user.full_name} исправил вакансию.")
        await like(message)


async def dislike(message: Message):
    """Ставим на счетчик."""
    try:
        ro_menu = {
            2: '1 неделя RO',
            3: '1 месяц RO',
            4: '6 месяцев RO',
            5: 'вечное RO',
        }
        admin_note = 'Рецидив от пользователя\n {user_data} \n Приговор: {verdict}'
    
        # Возможно ненужная проверка пересланное сообщение. Но админы иногда репостят вакухи.
        # И бот может быть не согласен с ними в правильности вакансии.
        recr_id = message.forward_from.id if message.is_forward(
        ) else message.from_id
    
        # Если рецидив:
        if recr_id in blacklist.keys():
            blacklist[recr_id] += 1
    
            user = message.from_user
            
            user_data = "{}, \n{}, \n{}".format(user.full_name, user.username, user.id)
            verdict = ro_menu.get(blacklist.get(recr_id))
    
            log.info(f"Рекрутер {message.from_user.full_name}\n" +
                     f"Количество нарушений: {blacklist.get(recr_id)}.")
    
            await bot.send_message(ADMIN, admin_note.format(user_data=user_data, verdict=verdict))
    
        else:
            blacklist[recr_id] = 1
            log.info(f"Рекрутер {message.from_user.full_name}: первое нарушение.")
    except:
        import traceback
        traceback.print_exc()

async def like(message: Message):
    "Снимаем со счетчика."
    
    recr_id = message.from_id
    
    # Пересланное ли сообщение и есть ли доступ к нему?
    if message.is_forward():
        if message.forward_from:
            recr_id = message.forward_from.id        

    # Убираем из черного списка.
    if recr_id in blacklist.keys():
        del (blacklist[recr_id])
        log.info(
            f"Рекрутер {message.from_user.full_name} правильно оформил вакансию"
            + " и убран и черного списка.")


def register_user(dp):
    dp.register_message_handler(handle)
