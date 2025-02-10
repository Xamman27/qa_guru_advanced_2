import requests
import pytest


@pytest.mark.parametrize("user_id, email",[(2, "janet.weaver@reqres.in")])
def test_user_data(user_id, email):
    url = f"http://0.0.0.0:8000/api/users/{user_id}"
    try:
        response = requests.get(url)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        body = response.json()
        data = body['data']

        assert data['email'] == email, f"Expected email {email}, but got {data['email']}"
        assert data['id'] == user_id, f"Expected id {user_id}, but got {data['id']}"
    except requests.exceptions.HTTPError as http_err:
        pytest.fail(f"HTTP error occurred: {http_err}")
    except Exception as err:
        pytest.fail(f"Other error occurred: {err}")

@pytest.mark.parametrize("email, password", [("george.bluth@reqres.in", "password123"),
                                             ("janet.weaver@reqres.in", "password456")])
def test_login(email, password):
    url = f"http://0.0.0.0:8000/api/login"
    json = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=json)
    assert response.status_code == 200
    assert 'token' in response.json()
    assert response.json()['token'] != ''


@pytest.mark.parametrize("email", ["george.bluth@reqres.in"])
def test_login_missing_password(email):
    url = f"http://0.0.0.0:8000/api/login"
    json = {"email": email, "password": ""}
    response = requests.post(url, json=json)
    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "Email and password are required"


@pytest.mark.parametrize("email, password", [("georg.bluth@reqres.in", "password123"),
                                             ("jane.weaver@reqres.in", "password456")])
def test_user_not_found(email, password):
    url = f"http://0.0.0.0:8000/api/login"
    json = {"email": email, "password": password}
    response = requests.post(url, json=json)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
