from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide

from bot.ports.http_client import HttpClient

from polymarket_sdk.client.polymarket_client import PolymarketHttpClient


class HttpProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_http_client(self) -> AsyncIterator[HttpClient]:
        client = PolymarketHttpClient()
        try:
            yield client
        finally:
            await client.aclose()
