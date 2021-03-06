from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from core.models import Receipe

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


def test_new_user_without_email_raises_error():
    """
    Test creating a new user without an email raises error
    """
    with pytest.raises(ValueError):
        get_user_model().objects.create_user(None, "test123")


def test_create_superuser_with_email_successful():
    """
    Test creating a new superuser with an email is successful
    """
    email = "test123@example.com"
    password = "Password123"
    user = get_user_model().objects.create_superuser(email=email, password=password)
    assert user.is_superuser is True
    assert user.is_staff is True


def test_create_recipe(normal_user):
    """
    Test creating a new recipe
    """
    recipe = Receipe.objects.create(
        title="Test recipe",
        time_minutes=10,
        price=Decimal("5.00"),
        user=normal_user,
        description="This is a test recipe",
    )
    assert recipe.title == "Test recipe"
