from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from usuario.serializers import UsuarioSerializer, AuthTokenSerializer


class CriarUsuarioView(generics.CreateAPIView):
    """Cria um novo usuário no sistema"""
    serializer_class = UsuarioSerializer


class CriarTokenView(ObtainAuthToken):
    """Cria um novo token de autenticação para o usuário"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class GerenciarUsuarioView(generics.RetrieveUpdateAPIView):
    """Gerencia um usuário autenticado"""
    serializer_class = UsuarioSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Recupera e retorna o usuário"""
        return self.request.user
