import asyncio
from dataclasses import dataclass
from typing import Any, Dict

from aiohttp import ClientSession


# TODO make param
HOST = "http://localhost:8080"


@dataclass
class ApiResponse:
    status: int
    data: Dict[str, Any]


async def api_get(uri: str) -> ApiResponse:
    async with ClientSession() as session:
        async with session.get(f"{HOST}{uri}") as response:
            return ApiResponse(
                status=response.status,
                data=await response.json(),
            )


def api_get_sync(uri: str) -> ApiResponse:
    return asyncio.run(api_get(uri))
