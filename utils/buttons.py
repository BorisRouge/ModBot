from aiogram import types


class Button:
    def __init__(self):
        self.cancel = self.set_cancel

    @property
    def set_cancel(self):
        button = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
        menu = types.InlineKeyboardMarkup(resize_keyboard=True).insert(button)
        return menu