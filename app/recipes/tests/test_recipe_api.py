from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from mixer.backend.django import mixer
from core.models import Receipe
from recipes.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPE_URL = reverse("recipes:recipe-list")


def get_detail_url(recipe_id):
    return reverse("recipes:recipe-detail", args=[recipe_id])


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
        self.user = mixer.blend(
            get_user_model(), email="example@test.com", password="testpass"
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
        """Test retrieving recipes for user"""
        mixer.blend(Receipe, user=self.user)

        response = self.client.get(RECIPE_URL)
        recipes = Receipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    def test_get_recipe_detail(self):
        """Test retrieving a recipe detail"""
        recipe = mixer.blend(Receipe, user=self.user)
        response = self.client.get(get_detail_url(recipe.id))
        serializer = RecipeDetailSerializer(recipe)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    def test_create_recipe(self):
        """Test creating a new recipe"""
        data = {
            "title": "Test recipe",
            "time_minutes": 30,
            "price": Decimal(5.00),
            "user": self.user.id,
            "description": "This is a test recipe",
        }
        response = self.client.post(RECIPE_URL, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Receipe.objects.count() == 1
        recipe = Receipe.objects.get(id=response.data["id"])
        assert recipe.title == data["title"]
        assert recipe.time_minutes == data["time_minutes"]
        assert recipe.price == data["price"]
        assert recipe.user == self.user
        assert recipe.description == data["description"]

    def test_partial_update(self):
        """Test updating a recipe with patch"""
        recipe = mixer.blend(Receipe, user=self.user)
        data = {"title": "New title"}
        response = self.client.patch(get_detail_url(recipe.id), data)
        assert response.status_code == status.HTTP_200_OK
        recipe.refresh_from_db()
        assert recipe.title == data["title"]

    def test_full_update(self):
        """Test updating a recipe with put"""
        recipe = mixer.blend(
            Receipe,
            user=self.user,
            title="Old title",
            time_minutes=30,
            price=Decimal(5.00),
            link="http://example.com",
        )
        data = {
            "title": "New title",
            "time_minutes": 60,
            "price": Decimal(10.00),
            "description": "This is a new description",
            "link": "http://example2.com",
        }
        response = self.client.put(get_detail_url(recipe.id), data)
        assert response.status_code == status.HTTP_200_OK
        recipe.refresh_from_db()
        assert recipe.title == data["title"]
        assert recipe.time_minutes == data["time_minutes"]
        assert recipe.price == data["price"]
        assert recipe.description == data["description"]

    def test_update_user_returns_error(self):
        """Test that a user cannot update another user's recipe"""
        other_user = mixer.blend(get_user_model())
        recipe = mixer.blend(Receipe, user=self.user)

        data = {
            "user": other_user.id,
        }
        response = self.client.patch(get_detail_url(recipe.id), data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_recipe(self):
        """Test deleting a recipe"""
        recipe = mixer.blend(Receipe, user=self.user)
        response = self.client.delete(get_detail_url(recipe.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Receipe.objects.count() == 0

    def test_delete_recipe_other_users_recipe_error(self):
        """Test that a user cannot delete another user's recipe"""
        other_user = mixer.blend(get_user_model())
        recipe = mixer.blend(Receipe, user=other_user)
        response = self.client.delete(get_detail_url(recipe.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND
