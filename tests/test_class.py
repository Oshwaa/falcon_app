import json
import pytest
import falcon
from falcon import testing
from app import app  # import your Falcon app
from schema import Item  # your Pydantic model

class TestItemResource:
    def setup_method(self):
        self.client = testing.TestClient(app)

    def test_get_items_empty(self):
        response = self.client.simulate_get("/items",headers={
                "Content-Type": "application/json",
                "Authorization": "TEST_TOKEN"
                })
        assert response.status == falcon.HTTP_200
        assert isinstance(response.json["items"], list)

    def test_post_valid_item(self):
        payload = {
            "name": "Sample Item",
            "quantity": 5
        }

        response = self.client.simulate_post(
            "/items",
            body=json.dumps(payload),
            headers={
                "Content-Type": "application/json",
                "Authorization": "TEST_TOKEN"
                }
        )

        assert response.status == falcon.HTTP_201
        assert response.json["item"]["name"] == payload["name"]
        assert response.json["item"]["quantity"] == payload["quantity"]

    def test_post_invalid_item(self):
        payload = {
            "name": "Missing quantity"
            # quantity is missing
        }

        response = self.client.simulate_post(
            "/items",
            body=json.dumps(payload),
            headers={
                "Content-Type": "application/json",
                "Authorization": "TEST_TOKEN"
                }
        )

        assert response.status == falcon.HTTP_400
        assert "error" in response.json
