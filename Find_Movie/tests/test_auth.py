import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
def test_registration():
    client = APIClient()
    data = {
        'username': 'testuser',
        'password': 'testpass123',
        'email': 'testuser@example.com'
    }

    response = client.post('/api/register/', data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username='testuser').exists()


@pytest.mark.django_db
def test_login_success():

    User.objects.create_user(username='testuser', password='testpass123')

    client = APIClient()
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }

    response = client.post('/api/login/', data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_login_failure():
    client = APIClient()
    data = {
        'username': 'wronguser',
        'password': 'wrongpass'
    }

    response = client.post('/api/login/', data, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'error' in response.data
