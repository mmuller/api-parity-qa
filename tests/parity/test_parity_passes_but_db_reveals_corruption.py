# test_parity_passes_but_db_reveals_corruption

import pytest
from validation.db_helper import DBHelper


@pytest.mark.parity
def test_parity_passes_but_db_reveals_corruption(
    payload, client_og, client_ng_with_bug
):
    """
    Demonstrates a critical limitation of response-based parity testing.
    Even when API responses match, underlying data may diverge.
    This test shows how silent corruption can pass unnoticed unless
    database validation is included.
    """

    og = client_og.post("/orders", payload)
    ng = client_ng_with_bug.post("/orders", payload)

    og_data = normalize_response(og.json())
    ng_data = normalize_response(ng.json())

    # but DB reveals the issue
    og_row = DBHelper.get_order_by_id(og.json()["order_id"])
    ng_row = DBHelper.get_order_by_id(ng.json()["order_id"])

    assert og_data == ng_data, "Responses differ unexpectedly"

    assert og_row != ng_row, (
        "Silent corruption not detected: " "parity passed but DB state diverged"
    )


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
