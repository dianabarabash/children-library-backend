import requests

BASE_URL = 'http://localhost/auth'


def test_authenticate_user():
    payload = {
        'email': 'validuser@example.com',
        'password': 'password123'
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 'session_id' in data


def test_authenticate_invalid_user():
    payload = {
        'email': 'invaliduser@example.com',
        'password': 'wrongpassword'
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 401
    data = response.json()
    assert data['message'] == 'Invalid credentials'
