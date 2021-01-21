import json
import pytest

from test.api_client import api_get, api_post, download_file, poll, upload_file


@pytest.mark.integration
def test_healthcheck():
    response = api_get("/")
    assert response.status == 200
    assert response.data == {"root": {"links": {"upload": "/api/documents"}}}


@pytest.mark.integration
def test_e2e():
    # Get upload url
    response = api_post("/api/documents", json=None)
    assert response.status == 201
    assert "documentUpload" in response.data

    upload_url = response.data["documentUpload"]["uploadUrl"]
    upload_headers = response.data["documentUpload"]["uploadHeaders"]
    result_uri = response.data["documentUpload"]["links"]["result"]

    # Upload test file
    upload_file(upload_url, upload_headers, file_name="test/resources/document.pdf")

    # Wait for result
    response = poll(
        callable=lambda: api_get(result_uri),
        condition=lambda api_response: api_response.status == 200,
    )
    assert response.status == 200
    assert "documentResult" in response.data

    result_url = response.data["documentResult"]["resultUrl"]

    # Download result file
    result = download_file(result_url)
    actual_json = json.loads(result)
    expected_json = json.load(open("test/resources/result.json"))
    assert actual_json == expected_json
