# test_data_parity

import pytest
from validation.db_helper import DBHelper


@pytest.mark.parity
def test_order_data_consistency(payload, client_og):
    """
    This test validates system-level consistency (API → DB).
    Full parity (OG vs NG) is covered in separate tests.
    """

    response = client_og.post("/orders", payload)
    order_id = response.json()["order_id"]

    row = DBHelper.get_order_by_id(order_id)

    assert row is not None
    assert float(row[1]) == payload["amount"]
