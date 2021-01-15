from typing import List

from aiohttp.web import Request, Response, RouteDef, get, json_response


def create_routes() -> List[RouteDef]:
    return [
        get("/", index),
    ]


async def index(request: Request) -> Response:
    return json_response({})
