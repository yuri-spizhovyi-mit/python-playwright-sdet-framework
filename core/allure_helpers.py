import json
import allure


def attach_json(name: str, data: dict):
    allure.attach(
        json.dumps(data, indent=2),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )
