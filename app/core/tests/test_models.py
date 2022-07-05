import pytest
from django.contrib.auth import get_user_model


pytestmark = pytest.mark.django_db


def test_create_user_with_email_successful():
    """
    Test creating a new user with an email is successful
    """
    email = "test@example.com"
    password = "Password123"
    user = get_user_model().objects.create_user(email=email, password=password)
    assert user.email == email
    assert user.check_password(password)


def test_new_user_email_normalized(sample_emails):
    """
    Test the email for a new user is normalized
    """
    for email, normalized_email in sample_emails:
        user = get_user_model().objects.create_user(email, "test123")
        assert user.email == normalized_email
