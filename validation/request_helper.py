import requests
from validation.config import BASE_URL


class RequestHelper:

    @staticmethod
    def post(path, payload=None, headers=None, expected_status=200):

        url = f"{BASE_URL}{path}"

        response = requests.post(url, json=payload, headers=headers or {})

        if isinstance(expected_status, (list, tuple)):
            assert response.status_code in expected_status, response.text
        else:
            assert response.status_code == expected_status, response.text

        return response
