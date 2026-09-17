from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from httpx import AsyncClient

from bot.transport.http.httpx_client import HttpxClient
from bot.ports.http_client import HttpClient


class HttpProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_http_client(self) -> AsyncIterator[HttpClient]:
        client = HttpxClient(AsyncClient())
        try:
            yield client
        finally:
            await client.aclose()
