# tests/contract/test_contract.py

import pytest
from validation.request_helper import RequestHelper
from jsonschema import validate
from schemas.order_schema import order_schema


@pytest.mark.contract
def test_create_order_schema(payload):
    response = RequestHelper.post("/orders", payload)

    validate(instance=response.json(), schema=order_schema)


@pytest.mark.contract
def test_response_tolerates_optional_fields(payload, client_og):
    """
    Validates observable API contract with tolerance for optional fields.

    Required:
    - amount
    - success

    Optional:
    - customer
    """

    response = client_og.post("/orders", payload)
    data = response.json()

    # required fields
    assert "amount" in data
    assert "success" in data

    # optional field
    assert "customer" not in data or isinstance(data["customer"], str)


@pytest.mark.contract
def test_response_does_not_expose_unexpected_fields(payload, client_og):

    response = client_og.post("/orders", payload)
    data = response.json()

    allowed_fields = {"amount", "success", "order_id"}

    assert set(data.keys()).issubset(allowed_fields)
