import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status


pytestmark = pytest.mark.django_db
CREATE_USER_URL = reverse("users:create")
TOKEN_URL = reverse("users:token")


def test_create_user_api_success(client):
    """Test creating a new user with an email is successful"""
    data = {
        "email": "test@example.com",
        "password": "Password123",
        "name": "Test",
    }
    response = client.post(CREATE_USER_URL, data)
    user = get_user_model().objects.get(email=data["email"])
    assert response.status_code == status.HTTP_201_CREATED
    assert user.check_password(data["password"]) is True
    assert "password" not in response.data


def test_user_with_email_exists_error(client):
    """Test creating a new user with an email that already exists raises error"""
    data = {
        "email": "test@example.com",
        "password": "Password123",
        "name": "Test",
    }
    get_user_model().objects.create_user(**data)
    response = client.post(CREATE_USER_URL, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_password_too_short_error(client):
    """Test creating a new user with a password that is too short raises error"""
    data = {
        "email": "test@example.com",
        "password": "pw12",
        "name": "Test",
    }
    response = client.post(CREATE_USER_URL, data)
    user_exists = get_user_model().objects.filter(email=data["email"]).exists()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert user_exists is False


def test_create_token_for_user(client, normal_user):
    """Test that a token is created for the user"""
    data = {"email": normal_user.email, "password": normal_user.password}
    response = client.post(TOKEN_URL, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["token"] is not None


def test_create_token_bad_credentials(client, normal_user):
    """Test returns an error for bad credentials"""
    data = {"email": normal_user.email, "password": "wrong"}
    response = client.post(TOKEN_URL, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["token"] is None
