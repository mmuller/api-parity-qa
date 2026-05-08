# test_logs_parity

import pytest
from validation.log_helper import LogHelper
from datetime import datetime


@pytest.mark.parity
def test_logs_parity(payload, client_og):

    start = datetime.now()

    response = client_og.post("/orders", payload)
    order_id = response.json()["order_id"]

    logs = LogHelper.wait_for_logs_since(start)
    logs_str = "\n".join(logs) if isinstance(logs, list) else logs

    assert f"Order created - id={order_id}" in logs_str
