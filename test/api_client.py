import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, TypeVar

import requests


T = TypeVar("T")
# TODO make param
HOST = "http://localhost:8080"


def poll(
    callable: Callable[[], T],
    condition: Callable[[T], bool],
    wait_time: int = 2,
    timeout: int = 60,
) -> T:
    # TODO timeout
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
        data=response.json() if response.content else {},
    )


def api_post(uri: str, json: Dict[str, Any]) -> ApiResponse:
    response = requests.post(f"{HOST}{uri}", json=json)
    return ApiResponse(
        status=response.status_code,
        data=response.json() if response.content else {},
    )


def download_file(url: str) -> str:
    response = requests.get(url)
    return response.text


def upload_file(url: str, file_name: str, headers: Dict[str, str]):
    with open(file_name, "rb") as file:
        requests.put(url, data=file, headers=headers)
