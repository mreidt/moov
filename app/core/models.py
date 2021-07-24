from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)


class GerenciadorUsuario(BaseUserManager):

    def create_user(self, email, nome, password=None, **extra_fields):
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
        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        usuario = self.create_user(email=email, password=password, nome=email)
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)

        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuário customizado, com login através do email"""
    email = models.EmailField(max_length=255, unique=True)
    nome = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = GerenciadorUsuario()

    USERNAME_FIELD = 'email'


class Empresa(models.Model):
    """Modelo de empresa"""
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)

    def __str__(self):
        return self.nome
