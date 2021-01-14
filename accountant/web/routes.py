from typing import List

from aiohttp.web import Request, Response, RouteDef, get, json_response, post

from accountant.util import generate_id


def create_routes() -> List[RouteDef]:
    return [
        post("/api/documents", create_upload_url),
        get("/api/documents/{document_id}", get_result),
    ]


async def create_upload_url(request: Request) -> Response:
    document_id = generate_id()
    # TODO generate signed S3 upload url
    upload_url = "upload-url"
    response = {
        "documentRequest": {
            "uploadUrl": upload_url,
            "resultUrl": f"/api/documents/{document_id}",
        }
    }
    return json_response(response, status=201)


async def get_result(request: Request) -> Response:
    document_id = request.match_info["document_id"]
    # TODO find document result
    response = {
        "documentResult": {
            "documentId": document_id,
            "statements": ["statement1", "statement2", "statement3"],
        }
    }
    return json_response(response)
