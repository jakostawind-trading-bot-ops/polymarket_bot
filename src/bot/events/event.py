from dataclasses import dataclass, field
from typing import ClassVar, Any
import time

@dataclass
class Event():
    event_type: ClassVar[str]
    event_name: ClassVar[str]
    payload: dict[str, Any]
    msg: str
    timestamp: int = field(default_factory=lambda: time.time_ns() // 1_000_000)