# test_orders_full_parity

import pytest
from validation.db_helper import DBHelper
from validation.log_helper import LogHelper
from datetime import datetime


def normalize_response(data):
    """
    Normalize response based on observable contract.

    Notes:
    - order_id is ignored (non-deterministic)
    - customer is optional / not always returned
    """

    return {
        "amount": data.get("amount"),
        "success": data.get("success"),
    }


def normalize_db(row):
    return {
        "amount": float(row[1]),
    }


@pytest.mark.parity
def test_full_system_parity(payload, client_og, client_ng):
    """
    Validates full system parity across:
    - API response (normalized)
    - Database state
    - Logs (per request)

    Notes:
    - order_id is ignored in response (non-deterministic)
    - logs must contain entries for both OG and NG executions
    """

    start = datetime.now()

    # --- API calls ---
    og_response = client_og.post("/orders", payload)
    ng_response = client_ng.post("/orders", payload)

    og_json = og_response.json()
    ng_json = ng_response.json()

    og_data = normalize_response(og_json)
    ng_data = normalize_response(ng_json)

    assert og_data == ng_data, "Response parity failed"

    # --- DB validation ---
    og_id = og_json["order_id"]
    ng_id = ng_json["order_id"]

    og_row = DBHelper.get_order_by_id(og_id)
    ng_row = DBHelper.get_order_by_id(ng_id)

    assert normalize_db(og_row) == normalize_db(ng_row), "DB parity failed"

    # --- LOG validation ---
    logs = LogHelper.wait_for_logs_since(start)
    logs_str = "\n".join(logs) if isinstance(logs, list) else logs

    assert f"id={og_id}" in logs_str, "Missing OG log entry"
    assert f"id={ng_id}" in logs_str, "Missing NG log entry"
