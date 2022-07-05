import pytest
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test_users_list(client, superuser, normal_user):
    """Test users list on admin page"""
    url = reverse("admin:core_user_changelist")
    client.force_login(superuser)
    response = client.get(url)

    assert normal_user.name in response.content.decode()
    assert normal_user.email in response.content.decode()


def test_edit_user_page(client, superuser, normal_user):
    """Test edit user page"""
    url = reverse("admin:core_user_change", args=[normal_user.id])
    client.force_login(superuser)
    response = client.get(url)

    assert response.status_code == 200
