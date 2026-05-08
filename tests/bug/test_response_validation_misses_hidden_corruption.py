# tests/bug/test_response_validation_misses_hidden_corruption.py

from validation.request_helper import RequestHelper


def test_response_validation_misses_hidden_corruption(payload):
    response = RequestHelper.post("/orders", payload)

    assert response.status_code == 200
