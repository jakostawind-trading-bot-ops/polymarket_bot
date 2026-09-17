from dataclasses import dataclass

@dataclass
class AccountState():
    # Account
    nickname: str
    wallet: str