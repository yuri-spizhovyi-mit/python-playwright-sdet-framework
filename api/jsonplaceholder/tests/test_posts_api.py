import json
import pytest
from jsonschema import validate
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
POST_SCHEMA = BASE_DIR / "schemas" / "post_schema.json"


@pytest.mark.api
def test_list_posts_schema(jsonplaceholder_client):
    response = jsonplaceholder_client.list_posts()
    assert response.status_code == 200

    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0

    schema = json.loads(POST_SCHEMA.read_text())

    for post in posts:
        validate(instance=post, schema=schema)
