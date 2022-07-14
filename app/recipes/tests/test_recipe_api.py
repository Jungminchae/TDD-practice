from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from mixer.backend.django import mixer
from core.models import Receipe
from recipes.serializers import RecipeSerializer


RECIPE_URL = reverse("recipes:recipe-list")


class PublicRecipeApiTests(APITestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth_to_retrieve_recipes(self):
        """Test that authentication is required to retrieve recipes"""
        response = self.client.get(reverse("recipes:recipe-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class PrivateRecipeApiTests(APITestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="normal_user1234@example.com",
            password="Password123",
            name="Test",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        mixer.cycle(3).blend(Receipe, user=self.user)
        response = self.client.get(RECIPE_URL)
        recipes = Receipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    def test_recipe_list_limited_to_user(self):
        mixer.blend(Receipe, user=self.user)

        response = self.client.get(RECIPE_URL)
        recipes = Receipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data
