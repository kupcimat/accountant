from test.api_client import api_get_sync


def test_healthcheck():
    response = api_get_sync("/")
    assert response.status == 200
    assert response.data == {"root": {"links": {"upload": "/api/documents"}}}
