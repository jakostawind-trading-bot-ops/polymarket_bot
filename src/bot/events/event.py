from dataclasses import dataclass, field
from typing import ClassVar, Any
import time
from uuid import UUID, uuid7

@dataclass
class Event():
    event_type: ClassVar[str]
    event_name: ClassVar[str]
    payload: dict[str, Any]
    msg: str
    trace_id: UUID = field(default_factory=uuid7)
    timestamp: int = field(default_factory=lambda: time.time_ns() // 1_000_000)