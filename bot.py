from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils import settings
from utils.rule_manager import RuleManager
from utils.logger import get_logger


log = get_logger()
config = settings.get_config('sample.env')
rm = RuleManager()
bot = Bot(token=config.telegram.telegram_bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())