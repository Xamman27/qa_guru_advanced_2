import requests
import pytest


def test_pagination_get_users_default(base_url):
    response = requests.get(f'{base_url}/users')
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 12
    assert type(data['items']) == list
    assert data['total'] == 12
    assert data['page'] == 1
    assert data['size'] == 50


def test_pagination_get_users_size_5(base_url):
    response = requests.get(f'{base_url}/users?size=5')
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 5
    assert type(data['items']) == list
    assert data['total'] == 12
    assert data['page'] == 1
    assert data['size'] == 5


def test_pagination_get_users_page_2_size_5(base_url):
    response = requests.get(f'{base_url}/users?page=2&size=5')
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 5
    assert type(data['items']) == list
    assert data['total'] == 12
    assert data['page'] == 2
    assert data['size'] == 5

def test_pagination_get_users_invalid_page(base_url):
    response = requests.get(f'{base_url}/users?page=9999&size=5')
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 0
    assert type(data['items']) == list
    assert data['total'] == 12
    assert data['page'] == 9999
    assert data['size'] == 5
    assert data['pages'] == 3


def test_pagination_get_users_no_duplicates(base_url):
    all_users = []
    page = 1
    size = 5

    while True:
        response = requests.get(f"{base_url}/users?page={page}&size={size}")
        assert response.status_code == 200
        data = response.json()
        all_users.extend(data['items'])

        if len(data['items']) < size:
            break

        page += 1

    user_ids = [user['id'] for user in all_users]
    assert len(user_ids) == len(set(user_ids))