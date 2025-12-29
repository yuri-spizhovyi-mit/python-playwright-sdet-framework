import json
from jsonschema import validate
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SCHEMA = BASE_DIR / "schemas" / "post_response_schema.json"


def test_post_echo_returns_payload(echo_client):
    payload = {
        "name": "sdet-framework",
        "type": "api-test",
    }

    response = echo_client.post_echo(payload)

    assert response.status_code == 200

    body = response.json()
    schema = json.loads(SCHEMA.read_text())

    validate(instance=body, schema=schema)
    assert body["json"] == payload
