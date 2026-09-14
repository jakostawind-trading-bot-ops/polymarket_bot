from dataclasses import dataclass
import secrets

from bot.lifecycle.bot_lifecycle.statuses import LifecycleStatus

def generate_bet_id():
    '''Генерирует рандомный бот ид'''
    CROCKFORD_BASE32_ALPHABET = "ABCDEFGHJKMNPQRSTVWXYZ"
    BOT_ID_LENGTH = 16
    return "".join(
        secrets.choice(CROCKFORD_BASE32_ALPHABET)
        for _ in range(BOT_ID_LENGTH)
    )

@dataclass
class GeneralState():
    bot_id: str
    bot_status: LifecycleStatus