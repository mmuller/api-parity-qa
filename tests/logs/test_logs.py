# tests/logs/test_logs.py

from validation.request_helper import RequestHelper
from datetime import datetime
from validation.log_helper import LogHelper


def test_logs_contain_correlation_id(payload):
    start_time = datetime.now()

    response = RequestHelper.post("/orders", payload)

    corr_id = response.headers.get("X-Correlation-ID")

    logs = LogHelper.wait_for_logs_since(start_time)

    assert f"[corr_id={corr_id}]" in logs
