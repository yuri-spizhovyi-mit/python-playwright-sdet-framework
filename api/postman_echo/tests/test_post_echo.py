import json
from jsonschema import validate
from pathlib import Path
import pytest
from core.allure_helpers import attach_json
from api.postman_echo.test_data import VALID_POST_PAYLOAD

BASE_DIR = Path(__file__).resolve().parents[1]
SCHEMA = BASE_DIR / "schemas" / "post_response_schema.json"


@pytest.mark.api
def test_post_echo_returns_payload(echo_client):
    response = echo_client.post_echo(VALID_POST_PAYLOAD)
    attach_json("request_payload", VALID_POST_PAYLOAD)
    attach_json("response_body", response.json())

    assert response.status_code == 200

    body = response.json()
    schema = json.loads(SCHEMA.read_text())

    validate(instance=body, schema=schema)
    assert body["json"] == VALID_POST_PAYLOAD
