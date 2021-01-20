import asyncio
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, TypeVar

from aiohttp import ClientSession


T = TypeVar("T")
# TODO make param
HOST = "http://localhost:8080"


def poll(
    callable: Callable[[], T], condition: Callable[[T], bool], wait_time: int = 2
) -> T:
    result = callable()
    while not condition(result):
        time.sleep(wait_time)
        result = callable()
    return result


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
