# tests/data/test_data_integrity.py

from validation.request_helper import RequestHelper
from validation.db_helper import DBHelper


def test_api_vs_db_amount(payload):
    response = RequestHelper.post("/orders", payload)

    data = response.json()
    order_id = data["order_id"]

    row = DBHelper.get_order_by_id(order_id)

    assert row[1] == data["amount"]
