from typing import List

from aiohttp.web import (
    HTTPAccepted,
    HTTPNotFound,
    Request,
    Response,
    RouteDef,
    get,
    json_response,
    post,
)

from accountant.util import generate_id
from accountant.storage import (
    create_curl,
    exists_object,
    generate_download_url,
    generate_upload_url,
)
from accountant.config import RESULT_BUCKET_NAME, UPLOAD_BUCKET_NAME
from accountant.web.models import DocumentResult, DocumentUpload, Root, serialize


def create_routes() -> List[RouteDef]:
    return [
        get("/", index),
        post("/api/documents", create_upload_url),
        get("/api/documents/{document_id}", get_result),
    ]


async def index(request: Request) -> Response:
    response = Root(links={"upload": "/api/documents"})
    return json_response(serialize(response))


async def create_upload_url(request: Request) -> Response:
    document_id = generate_id()
    presigned_url = generate_upload_url(UPLOAD_BUCKET_NAME, document_id)
    response = DocumentUpload(
        uploadUrl=presigned_url.url,
        uploadParams=presigned_url.params,
        uploadCurl=create_curl(presigned_url),
        links={"result": f"/api/documents/{document_id}"},
    )
    return json_response(serialize(response), status=201)


async def get_result(request: Request) -> Response:
    document_id = request.match_info["document_id"]
    if exists_object(RESULT_BUCKET_NAME, document_id) is False:
        if exists_object(UPLOAD_BUCKET_NAME, document_id) is False:
            raise HTTPNotFound()
        else:
            raise HTTPAccepted()

    presigned_url = generate_download_url(RESULT_BUCKET_NAME, document_id)
    response = DocumentResult(
        resultUrl=presigned_url.url,
        links={"result": f"/api/documents/{document_id}"},
    )
    return json_response(serialize(response))
