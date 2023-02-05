from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.dispatcher import FSMContext
from bot import bot, config, rm
from utils.states import StateAdmin
from utils.buttons import Button

async def get_rules(message: Message):
    """Выгружает файл с правилами по команде администратора в его личку."""
    rules_file = InputFile(config.rules.path)
    await bot.send_document(message.from_id, rules_file)

    
async def set_rules(message: Message, state: FSMContext):
    """Загружает файл с правилами в бота по указанному в файле настроек адресу."""
    # Небольшая проверка на наличие файла и то, что направлен правильный (только по названию).
    if message.document.file_name == config.rules.file_name:  # https://docs.aiogram.dev/en/latest/_modules/aiogram/types/document.html?highlight=helper.Item()
        await message.document.download(config.rules.path)
        await state.reset_state()
        rm.refresh_rules()
        await message.answer('Правила обновлены.')
    else:
        await message.answer('Проверьте название файла, операция отменена.')
        await state.reset_state()

    
async def initiate_set_rules(message: Message):
    """Начало операции обновления файла правил."""
    await message.answer('Выгрузите файл с правилами',
                         reply_markup=Button().cancel)
    await StateAdmin.R1.set()
    
    
async def cancel_button(callback: CallbackQuery, state: FSMContext):
    """Логика кнопки отмены"""
    await state.reset_state()
    await bot.send_message(callback.from_user.id, 'Операция отменена.')


def register_admin(dp):
    dp.register_message_handler(get_rules,
                                user_id=config.telegram.admin,
                                commands=['get'],
                                state='*'
                                )
    dp.register_message_handler(initiate_set_rules,
                                user_id=config.telegram.admin,
                                commands=['set'],
                                state='*'
                                )
    dp.register_message_handler(set_rules,
                                user_id=config.telegram.admin,
                                content_types='document',
                                state=StateAdmin.R1
                                )
    dp.register_callback_query_handler(cancel_button, text='cancel', state='*')
