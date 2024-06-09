import requests
import pytest

AUTH_URL = 'http://localhost/auth'


@pytest.fixture
def f_session_id():
    payload = {
        'email': 'validuser@example.com',
        'password': 'password123'
    }
    response = requests.post(AUTH_URL, json=payload)
    assert response.status_code == 200
    data = response.json()
    return data['session_id']


class TestBooks:
    BASE_URL = 'http://localhost/books'

    def test_get_books(self, f_session_id):
        headers = {'Session-ID': f_session_id}
        response = requests.get(self.BASE_URL, headers=headers)
        assert response.status_code == 200
        assert response.json() == [
            {
                'age': 10,
                'cover': '/path/to/cover1.jpg',
                'description': 'This is an example book description.',
                'id': 1,
                'lang': 'ENG',
                'pages': 300,
                'title': 'Example Book 1',
            },
            {
                'age': 5,
                'cover': '/path/to/cover2.jpg',
                'description': 'This is another example book description.',
                'id': 2,
                'lang': 'UKR',
                'pages': 150,
                'title': 'Example Book 2',
            },
            {
                'age': 15,
                'cover': '/path/to/cover3.jpg',
                'description': 'This is another example book description.',
                'id': 3,
                'lang': 'GER',
                'pages': 100,
                'title': 'Example Book 3',
            },
            {
                'age': 12,
                'cover': '/path/to/cover4.jpg',
                'description': 'This is another example book description.',
                'id': 4,
                'lang': 'ENG',
                'pages': 120,
                'title': 'Example Book 4',
            },
            {
                'age': 25,
                'cover': '/path/to/cover5.jpg',
                'description': 'This is another example book description.',
                'id': 5,
                'lang': 'UKR',
                'pages': 150,
                'title': 'Example Book 5',
            },
            {
                'age': 35,
                'cover': '/path/to/cover6.jpg',
                'description': 'This is another example book description.',
                'id': 6,
                'lang': 'GER',
                'pages': 90,
                'title': 'Example Book 6',
            }

        ]


class TestBook:
    BASE_URL = 'http://localhost/book'

    def test_create_book(self, f_session_id):
        headers = {'Session-ID': f_session_id}
        payload = {
            'title': 'Test Book',
            'lang': 'ENG',
            'age': 1,
            'pages': 100,
            'description': 'A test book description.',
            'cover': 'path/to/cover.jpg'
        }
        response = requests.post(self.BASE_URL, json=payload, headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert 'id' in data
        assert data['title'] == 'Test Book'

    def test_get_book(self, f_session_id):
        url = f"{self.BASE_URL}/1"  # Assuming the book with id 1 exists
        headers = {'Session-ID': f_session_id}
        response = requests.get(url, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data['title'] == 'Example Book 1'

    def test_delete_book(self, f_session_id):
        url = f"{self.BASE_URL}/1"  # Assuming the book with id 1 exists
        headers = {'Session-ID': f_session_id}
        response = requests.delete(url, headers=headers)
        assert response.status_code == 204

    def test_delete_nonexistent_book(self, f_session_id):
        url = f"{self.BASE_URL}/9999"  # Assuming the book with id 9999 does not exist
        headers = {'Session-ID': f_session_id}
        response = requests.delete(url, headers=headers)
        assert response.status_code == 404


class TestUserBook:
    BOOK_ID = 3

    def test_get(self, f_session_id):
        headers = {'Session-ID': f_session_id}
        response = requests.get(f"http://localhost/book/{self.BOOK_ID}/user", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data == {'end_date': "None", 'id': 3, 'start_date': "None"}

    def test_delete(self, f_session_id):
        headers = {'Session-ID': f_session_id}
        response = requests.delete(f"http://localhost/book/{self.BOOK_ID}/user", headers=headers)
        assert response.status_code == 204
        assert not response.text

    def test_put(self, f_session_id):
        headers = {'Session-ID': f_session_id}
        response = requests.put(f"http://localhost/book/{self.BOOK_ID}/user", headers=headers)
        assert response.status_code == 201
        assert response.json() == {'message': 'Book created successfully', 'book_id': self.BOOK_ID}


class TestUserBookStartReading:
    BOOK_ID = 3
    BOOK_ID_NOT_IN_LIST = 2
    BOOK_ID_ALREADY_READ = 4

    def test_post_not_in_reading_list(self, f_session_id):
        headers = {'Session-ID': f_session_id}
        response = requests.post(f"http://localhost/book/{self.BOOK_ID_NOT_IN_LIST}/user/start", headers=headers)
        assert response.status_code == 400
        assert response.json() == {'message': 'Book is not in the reading list', 'book_id': self.BOOK_ID_NOT_IN_LIST}

    def test_post_start_reading(self, f_session_id):
        headers = {'Session-ID': f_session_id}
        response = requests.post(f"http://localhost/book/{self.BOOK_ID}/user/start", headers=headers)
        assert response.status_code == 201
        assert response.json() == {'message': 'You have started reading the book', 'book_id': self.BOOK_ID}

    def test_post_start_reading_already_read(self, f_session_id):
        headers = {'Session-ID': f_session_id}
        response = requests.post(f"http://localhost/book/{self.BOOK_ID_ALREADY_READ}/user/start", headers=headers)
        assert response.status_code == 400
        assert response.json() == {'message': 'Book has been already read', 'book_id': self.BOOK_ID_ALREADY_READ}


class TestUserBookStopReading:
    BOOK_ID_NOT_IN_LIST = 2
    BOOK_ID_NOT_STARTED = 5
    BOOK_ID_ALREADY_STARTED = 6

    def test_post_not_in_reading_list(self, f_session_id):
        headers = {'Session-ID': f_session_id}
        response = requests.post(f"http://localhost/book/{self.BOOK_ID_NOT_IN_LIST}/user/end", headers=headers)
        assert response.status_code == 400
        assert response.json() == {'message': 'Book is not in the reading list', 'book_id': self.BOOK_ID_NOT_IN_LIST}

    def test_post_not_started_reading(self, f_session_id):
        headers = {'Session-ID': f_session_id}
        response = requests.post(f"http://localhost/book/{self.BOOK_ID_NOT_STARTED}/user/end", headers=headers)
        assert response.status_code == 400
        assert response.json() == {'message': 'You have not started reading the book',
                                   'book_id': self.BOOK_ID_NOT_STARTED}

    def test_post_stopped_reading(self, f_session_id):
        headers = {'Session-ID': f_session_id}
        response = requests.post(f"http://localhost/book/{self.BOOK_ID_ALREADY_STARTED}/user/end", headers=headers)
        assert response.status_code == 201
        assert response.json() == {'message': 'You have finished reading the book',
                                   'book_id': self.BOOK_ID_ALREADY_STARTED}
