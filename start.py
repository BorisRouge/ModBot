from aiogram import executor
from bot import dp
from handlers.user import register_user
from handlers.admin import register_admin


register_admin(dp)
register_user(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)