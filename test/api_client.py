import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, TypeVar

import requests


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


def api_get(uri: str) -> ApiResponse:
    response = requests.get(f"{HOST}{uri}")
    return ApiResponse(
        status=response.status_code,
        data=response.json(),
    )
