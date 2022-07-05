import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def sample_emails():
    return [
        ["test1@EXAMPLE.com", "test1@example.com"],
        ["Test2@Example.com", "Test2@example.com"],
        ["TEST3@EXAMPLE.com", "TEST3@example.com"],
        ["test4@example.com", "test4@example.com"],
    ]


@pytest.fixture
def normal_user():
    return get_user_model().objects.create_user(
        email="normal_user123@example.com", password="Password123", name="Test"
    )


@pytest.fixture
def superuser():
    return get_user_model().objects.create_superuser(
        email="admin_123@example.com", password="Password123"
    )
