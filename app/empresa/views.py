from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Empresa, Motorista
from empresa import serializers


class EmpresaViewSet(viewsets.ModelViewSet):
    """Gerencia as empresas na base de dados"""
    serializer_class = serializers.EmpresaSerializer
    queryset = Empresa.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Cria uma nova empresa"""
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class MotoristaViewSet(viewsets.ModelViewSet):
    """Gerencia os motoristas na base de dados"""
    serializer_class = serializers.MotoristaSerializer
    queryset = Motorista.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Cria um novo motorista"""
        serializer.save()


# class RecipeViewSet(viewsets.ModelViewSet):
#     """Manage recipes in the database"""
#     serializer_class = serializers.RecipeSerializer
#     queryset = Recipe.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def _params_to_ints(self, qs):
#         """Convert a list of string IDs to a list of integers"""
#         return [int(str_id) for str_id in qs.split(',')]

#     def get_queryset(self):
#         """Retrieve the recipes for the authenticated user"""
#         tags = self.request.query_params.get('tags')
#         ingredients = self.request.query_params.get('ingredients')
#         queryset = self.queryset
#         if tags:
#             tag_ids = self._params_to_ints(tags)
#             queryset = queryset.filter(tags__id__in=tag_ids)
#         if ingredients:
#             ingredient_ids = self._params_to_ints(ingredients)
#             queryset = queryset.filter(ingredients__id__in=ingredient_ids)

#         return queryset.filter(user=self.request.user)

#     def get_serializer_class(self):
#         """Return appropriate serializer class"""
#         if self.action == 'retrieve':
#             return serializers.RecipeDetailSerializer
#         elif self.action == 'upload_image':
#             return serializers.RecipeImageSerializer

#         return self.serializer_class

#     def perform_create(self, serializer):
#         """Create a new recipe"""
#         serializer.save(user=self.request.user)
