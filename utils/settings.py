from dataclasses import dataclass
from environs import Env


@dataclass
class Rules:
   file_name: str
   path: str


@dataclass
class Telegram:
    telegram_bot_token: str
    admin: str


@dataclass
class Settings:
    telegram: Telegram
    rules: Rules


def get_config(path: str = None):
    """Получение переменных из указанной среды."""
    env = Env()
    env.read_env(path)
    return Settings(
        telegram=Telegram(
            telegram_bot_token=env.str('TELEGRAM_BOT_TOKEN'),
            admin=env.str('TELEGRAM_ADMIN'),
        ),
        rules=Rules(
            file_name=env.str('RULES_FILENAME'),
            path=env.str('RULES_PATH'),
        ),
    )
