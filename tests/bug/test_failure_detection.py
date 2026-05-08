# test_failure_detection

import pytest
import threading
from validation.request_helper import RequestHelper
from validation.db_helper import DBHelper
from validation.log_helper import LogHelper
from datetime import datetime


@pytest.mark.bug
def test_should_detect_silent_data_corruption(payload):

    response = RequestHelper.post(
        "/orders", payload, headers={"x-bug-mode": "silent_db_bug"}
    )

    data = response.json()
    order_id = data["order_id"]

    row = DBHelper.get_order_by_id(order_id)
    db_amount = row[1]

    assert (
        db_amount == payload["amount"]
    ), f"Silent corruption detected: DB={db_amount}, expected={payload['amount']}"


@pytest.mark.bug
def test_should_detect_missing_logs(payload):

    start_time = datetime.now()

    response = RequestHelper.post(
        "/orders", payload, headers={"x-bug-mode": "missing_log"}
    )

    data = response.json()
    order_id = data["order_id"]

    logs = LogHelper.wait_for_logs_since(start_time)

    assert f"Order created - id={order_id}" in logs, "Missing critical log info"


@pytest.mark.bug
def test_should_detect_duplicate_correlation_ids(payload):

    start_time = datetime.now()

    def call():
        RequestHelper.post(
            "/orders", payload, headers={"x-bug-mode": "bad_correlation"}
        )

    threads = [threading.Thread(target=call) for _ in range(10)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    logs = LogHelper.wait_for_logs_since(start_time)

    ids = LogHelper.extract_correlation_ids(logs)

    assert len(ids) == len(
        set(ids)
    ), "Duplicate correlation IDs detected (concurrency issue)"
