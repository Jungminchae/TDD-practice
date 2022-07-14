from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipes.views import RecipeViewSet


router = DefaultRouter()
router.register("recipes", RecipeViewSet, basename="recipe")

app_name = "recipes"

urlpatterns = [
    path("", include(router.urls)),
]
