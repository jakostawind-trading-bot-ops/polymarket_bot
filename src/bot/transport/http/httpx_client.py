from collections.abc import Mapping

from httpx import AsyncClient

from bot.ports.http_client import HttpClient, HttpResponse


class HttpxClient(HttpClient):
    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        json: object | None = None,
    ) -> HttpResponse:
        return await self._client.request(
            method,
            url,
            params=params,
            headers=headers,
            json=json,
        )

    async def aclose(self) -> None:
        await self._client.aclose()
