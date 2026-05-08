# test_orders_validation

import pytest
from validation.request_helper import RequestHelper
from validation.db_helper import DBHelper


@pytest.mark.negative
@pytest.mark.bug
def test_invalid_input_should_not_be_persisted(payload):

    invalid_payload = payload.copy()
    invalid_payload["amount"] = -100

    response = RequestHelper.post("/orders", invalid_payload)

    data = response.json()
    order_id = data["order_id"]

    assert data["amount"] >= 0, f"Invalid amount accepted: {data['amount']}"

    row = DBHelper.get_order_by_id(order_id)
    assert row[1] >= 0, f"Invalid amount persisted in DB: {row[1]}"
