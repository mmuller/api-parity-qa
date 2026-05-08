import pytest
from validation.parity_clients import ClientOG, ClientNG


@pytest.fixture
def payload():
    return {"customer": "Mauricio", "amount": 100.5}


@pytest.fixture
def client_og():
    return ClientOG()


@pytest.fixture
def client_ng():
    return ClientNG()


@pytest.fixture
def client_ng_with_bug():
    return ClientNG(bug_mode="silent_db_bug")
