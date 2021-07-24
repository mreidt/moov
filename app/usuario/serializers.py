from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para os objetos usuário"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'nome')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """Cria um novo usuário com senha encriptada e retorna ele"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Faz update em um usuário, setando a senha corretamente e retorna ele
        """
        password = validated_data.pop('password', None)
        usuario = super().update(instance, validated_data)

        if password:
            usuario.set_password(password)
            usuario.save()

        return usuario


class AuthTokenSerializer(serializers.Serializer):
    """Serializer para o objeto de autenticação de usuário"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    nome = serializers.CharField()

    def validate(self, attrs):
        """Valida e autentica o usuário"""
        email = attrs.get('email')
        password = attrs.get('password')
        nome = attrs.get('password')

        usuario = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
            nome=nome
        )
        if not usuario:
            mensagem = _(
                'Não foi possível autenticar com as credenciais fornecidas.'
            )
            raise serializers.ValidationError(mensagem, code='authentication')

        attrs['user'] = usuario
        return attrs
