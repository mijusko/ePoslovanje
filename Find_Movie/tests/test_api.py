import pytest
import requests
import requests_mock


BASE_URL = 'https://api.themoviedb.org/3'
API_KEY = '63b3cc9d929f980aaaf1c0d256057c3f'


def search_movies(query):
    url = f'{BASE_URL}/search/movie?query={query}&api_key={API_KEY}'
    return requests.get(url)


def get_trending_movies():
    url = f'{BASE_URL}/trending/movie/week?api_key={API_KEY}'
    return requests.get(url)


def get_movie_details(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}?api_key={API_KEY}'
    return requests.get(url)


def test_search_movies():
    with requests_mock.Mocker() as m:
        m.get(f'{BASE_URL}/search/movie?query=Inception&api_key={API_KEY}',
              json={'results': []})
        response = search_movies('Inception')
        assert response.status_code == 200
        assert response.json() == {'results': []}


def test_get_trending_movies():
    with requests_mock.Mocker() as m:
        m.get(f'{BASE_URL}/trending/movie/week?api_key={API_KEY}',
              json={'results': []})
        response = get_trending_movies()
        assert response.status_code == 200
        assert response.json() == {'results': []}


def test_get_movie_details():
    with requests_mock.Mocker() as m:
        m.get(f'{BASE_URL}/movie/123?api_key={API_KEY}', json={'id': 123})
        response = get_movie_details(123)
        assert response.status_code == 200
        assert response.json() == {'id': 123}
