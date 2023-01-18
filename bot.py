from aiogram import Bot, Dispatcher
from utils import settings
from utils.rules import RuleManager
from utils.logger import get_logger


log = get_logger()
config = settings.get_config('sample.env')
rm = RuleManager()
bot = Bot(token=config.telegram.telegram_bot_token)
dp = Dispatcher(bot)