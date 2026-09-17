from collections.abc import Mapping
from typing import Any, Protocol


class HttpResponse(Protocol):
    @property
    def status_code(self) -> int: ...

    def json(self) -> Any: ...


class HttpClient(Protocol):
    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        json: object | None = None,
    ) -> HttpResponse: ...

    async def aclose(self) -> None: ...
