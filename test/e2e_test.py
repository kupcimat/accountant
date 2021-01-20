import pytest

from test.api_client import api_get


@pytest.mark.integration
def test_healthcheck():
    response = api_get("/")
    assert response.status == 200
    assert response.data == {"root": {"links": {"upload": "/api/documents"}}}
