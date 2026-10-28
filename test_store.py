from base_request import api

new_order = {
    "id": 70707,
    "petId": 555001,
    "quantity": 1,
    "shipDate": "2026-10-30T09:30:00.000+00:00",
    "status": "approved",
    "complete": False,
}


def test_add_order():
    response = api.post("store/order", new_order)
    print("POST /store/order:", response.status_code, response.text)
    assert response.status_code == 200
    assert response.json()["status"] == "approved"


def test_find_order():
    response = api.get(f"store/order/{new_order['id']}")
    print("GET /store/order:", response.status_code, response.text)
    assert response.status_code == 200
    assert response.json()["id"] == new_order["id"]


def test_inventory():
    response = api.get("store/inventory")
    print("GET /store/inventory:", response.status_code, response.text)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_remove_order():
    response = api.delete(f"store/order/{new_order['id']}")
    print("DELETE /store/order:", response.status_code, response.text)
    assert response.status_code == 200

    check = api.get(f"store/order/{new_order['id']}", expected_error=True)
    assert check.status_code == 404
