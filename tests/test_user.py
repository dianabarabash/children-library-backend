import requests

BASE_URL = 'http://localhost/user'


def test_register_user():
    payload = {
        'email': 'testuser1234@example.com',
        'password': 'password123'
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['message'] == 'User created successfully'
    assert 'user_id' in data


def test_register_existing_user():
    payload = {
        'email': 'testuser1234@example.com',
        'password': 'password123'
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data['message'] == 'User already exists'


def test_register_no_email():
    payload = {
        'password': 'password123'
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data['message'] == {'email': 'Email is required'}


def test_register_no_password():
    payload = {
        'email': 'testuser1234@example.com',
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data['message'] == {'password': 'Password is required'}
