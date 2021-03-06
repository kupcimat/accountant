from dataclasses import asdict
from typing import Dict, List

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

from accountant.config import RESULT_BUCKET_NAME, UPLOAD_BUCKET_NAME
from accountant.storage import (
    create_download_curl,
    create_upload_curl,
    exists_object,
    generate_download_url,
    generate_upload_url,
)
from accountant.util import generate_id, serialize
from accountant.web.models import DocumentRequest, DocumentResult, DocumentUpload, Root


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
    metadata = asdict(DocumentRequest(documentType="document:kb:pdf"))

    presigned_url = generate_upload_url(UPLOAD_BUCKET_NAME, document_id, metadata)
    presigned_headers = create_headers(metadata)
    response = DocumentUpload(
        uploadUrl=presigned_url,
        uploadHeaders=presigned_headers,
        uploadCurl=create_upload_curl(presigned_url, presigned_headers),
        links={"result": f"/api/documents/{document_id}"},
    )
    return json_response(serialize(response), status=201)


async def get_result(request: Request) -> Response:
    document_id = request.match_info["document_id"]
    if exists_object(RESULT_BUCKET_NAME, document_id) is False:
        if exists_object(UPLOAD_BUCKET_NAME, document_id) is False:
            raise HTTPNotFound(text="")
        else:
            raise HTTPAccepted(text="")

    presigned_url = generate_download_url(RESULT_BUCKET_NAME, document_id)
    response = DocumentResult(
        resultUrl=presigned_url,
        resultCurl=create_download_curl(presigned_url),
        links={"result": f"/api/documents/{document_id}"},
    )
    return json_response(serialize(response))


def create_headers(metadata: Dict[str, str]) -> Dict[str, str]:
    return {f"x-amz-meta-{key}": value for key, value in metadata.items()}
