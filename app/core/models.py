from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)


class GerenciadorUsuario(BaseUserManager):

    def cria_usuario(self, email, nome, senha=None, **extra_fields):
        """Cria e salva um novo usuário"""
        if not email:
            raise ValueError('Usuários devem ter um email válido.')
        if not nome:
            raise ValueError('Usuários devem ter um nome válido.')
        usuario = self.model(
            email=self.normalize_email(email),
            nome=nome,
            **extra_fields
        )
        usuario.set_password(senha)
        usuario.save(using=self._db)

        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuário customizado, com login através do email"""
    email = models.EmailField(max_length=255, unique=True)
    nome = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    objects = GerenciadorUsuario()

    USERNAME_FIELD = 'email'
