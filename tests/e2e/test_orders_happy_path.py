# tests/e2e/test_orders_happy_path.py
import pytest
from validation.request_helper import RequestHelper
from datetime import datetime
from validation.db_helper import DBHelper
from validation.log_helper import LogHelper


@pytest.mark.happy_path
def test_create_order_e2e(payload):

    start_time = datetime.now()

    response = RequestHelper.post("/orders", payload)

    assert response.status_code == 200

    data = response.json()
    order_id = data["order_id"]

    # DB
    row = DBHelper.get_order_by_id(order_id)
    assert row is not None

    # Logs
    logs = LogHelper.wait_for_logs_since(start_time)
    assert f"Order created - id={order_id}" in logs
