from rest_framework import serializers
from core.models import Receipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""

    class Meta:
        model = Receipe
        fields = ("id", "title", "time_minutes", "price", "user", "link")
        read_only_fields = ("user",)
        extra_kwargs = {
            "id": {"read_only": True},
            "title": {"required": True},
            "time_minutes": {"required": True},
            "price": {"required": True},
            "user": {"read_only": True},
            "link": {"read_only": True},
        }


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe objects"""

    class Meta:
        model = Receipe
        fields = RecipeSerializer.Meta.fields + ("description",)
