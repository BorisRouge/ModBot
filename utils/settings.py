from dataclasses import dataclass
import os


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
    return Settings(
        telegram=Telegram(
            telegram_bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
            admin=os.getenv('TELEGRAM_ADMIN'),
        ),
        rules=Rules(
            file_name=os.getenv('RULES_FILENAME'),
            path=os.getenv('RULES_PATH'),
        ),
    )
