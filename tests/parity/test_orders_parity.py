# test_orders_parity

import pytest


@pytest.mark.parity
def test_orders_response_parity(payload, client_og, client_ng):

    og_response = client_og.post("/orders", payload)
    ng_response = client_ng.post("/orders", payload)

    assert og_response.status_code == ng_response.status_code

    og_data = normalize_response(og_response.json())
    ng_data = normalize_response(ng_response.json())

    assert og_data == ng_data


def normalize_response(data):
    normalized = {
        "amount": data.get("amount"),
        "success": data.get("success"),
    }

    # Optional fields (tolerated)
    optional_fields = ["customer"]

    for field in optional_fields:
        if field in data:
            normalized[field] = data[field]

    return normalized
