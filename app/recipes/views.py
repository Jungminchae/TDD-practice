from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Receipe
from recipes.serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    """ViewSet for manage recipe APIs"""

    serializer_class = RecipeSerializer
    queryset = Receipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-id")
