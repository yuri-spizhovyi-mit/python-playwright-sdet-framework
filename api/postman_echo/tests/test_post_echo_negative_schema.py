import json
import pytest
from jsonschema import validate, ValidationError
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INVALID_SCHEMA = BASE_DIR / "schemas" / "post_response_invalid_schema.json"


@pytest.api
def test_post_echo_fails_schema_validation(echo_client):
    payload = {"key": "value"}

    response = echo_client.post_echo(payload)
    assert response.status_code == 200

    body = response.json()
    schema = json.loads(INVALID_SCHEMA.read_text())

    with pytest.raises(ValidationError):
        validate(instance=body, schema=schema)
