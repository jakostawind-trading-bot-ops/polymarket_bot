from dataclasses import dataclass, field
import time
from uuid import UUID, uuid7

@dataclass(kw_only=True)
class Event():
    message_id: UUID = field(default_factory=uuid7)
    trace_id: str = field(default_factory=lambda: str(uuid7()))
    timestamp: int = field(default_factory=lambda: time.time_ns() // 1_000_000)
