from base_request import api

new_user = {
    "id": 20402,
    "username": "priz_student",
    "firstName": "Andrey",
    "lastName": "Priz",
    "email": "priz@student.ru",
    "password": "password1",
    "phone": "9007654321",
    "userStatus": 1,
}


def test_add_user():
    response = api.post("user", new_user)
    print("POST /user:", response.status_code, response.text)
    assert response.status_code == 200


def test_find_user():
    response = api.get(f"user/{new_user['username']}")
    print("GET /user:", response.status_code, response.text)
    assert response.status_code == 200
    assert response.json()["email"] == new_user["email"]


def test_edit_user():
    changed = new_user.copy()
    changed["phone"] = "9000000001"
    response = api.put(f"user/{new_user['username']}", changed)
    print("PUT /user:", response.status_code, response.text)
    assert response.status_code == 200

    check = api.get(f"user/{new_user['username']}")
    assert check.json()["phone"] == "9000000001"


def test_remove_user():
    response = api.delete(f"user/{new_user['username']}")
    print("DELETE /user:", response.status_code, response.text)
    assert response.status_code == 200

    check = api.get(f"user/{new_user['username']}", expected_error=True)
    assert check.status_code == 404
