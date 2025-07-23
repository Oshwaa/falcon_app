import falcon
from falcon import testing
import pytest
from app import app,items
from pydantic import ValidationError

@pytest.fixture
def client():
    return testing.TestClient(app)

def test_get_items_initially_empty(client):
    response = client.simulate_get('/items',headers={
                "Content-Type": "application/json",
                "Authorization": "TEST_TOKEN"
                })
    assert response.status == falcon.HTTP_200
    assert response.json == {"items": []}


def test_unauthorized_post_items(client):
    payload = {
        "name": "banana",
        "quantity": 2
    }
    response = client.simulate_post(
        '/items',json=payload,
        headers={
            "Content-Type":"application/json",
        }
        )
    
    assert response.status == falcon.HTTP_401
    assert "Invalid" in response.json['description']

def test_post_valid_item(client):
    payload = {
        "name": "banana",
        "quantity": 2
    }
    response = client.simulate_post('/items', json=payload,headers={
                "Content-Type": "application/json",
                "Authorization": "TEST_TOKEN"
                })

    assert response.status == falcon.HTTP_201
    assert "item" in response.json
    # to check response
    assert response.json["item"]["name"] == "banana"
    assert response.json["item"]["quantity"] == 2

def test_post_missing_name(client):
    payload = {}  # Missing 'name'
    response = client.simulate_post('/items', json=payload,headers={
                "Content-Type": "application/json",
                "Authorization": "TEST_TOKEN"
                })

    assert response.status == falcon.HTTP_400
    assert "error" in response.json


def test_input_error(client): 
    payload = {
        "name": 1,
        "quantity": "test"
    }

    response = client.simulate_post('/items', json=payload,
                                    headers={
                "Content-Type": "application/json",
                "Authorization": "TEST_TOKEN"
                })

    assert response.status_code == 400
    assert "error" in response.json
    assert any("name" in str(err["loc"]) for err in response.json["error"])


#this test is to mock an insert to an external database
def test_post_logs_item(client, mocker):
    
    items.clear()
    payload = {"name": "MockItem", "quantity": 2}

    
    mocked_logger = mocker.patch("app.log_item_addition")

    
    response = client.simulate_post("/items", json=payload,headers={
                "Content-Type": "application/json",
                "Authorization": "TEST_TOKEN"
                })

    assert response.status == falcon.HTTP_201
    mocked_logger.assert_called_once_with({"name": "MockItem", "quantity": 2})

