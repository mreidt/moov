from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_criando_usuario_com_sucesso(self):
        """Testa a criação de um usuário com sucesso"""
        email = 'teste123@gmail.com'
        password = 'teste123'
        nome = 'usuario 123'
        usuario = get_user_model().objects.create_user(
            email=email,
            password=password,
            nome=nome
        )

        self.assertEqual(usuario.email, email)
        self.assertTrue(usuario.check_password(password))
        self.assertEqual(usuario.nome, nome)

    def test_cria_usuario_email_normalizado(self):
        """Testa o funcionamento da normalização de email"""
        email = 'teste123@GMAIL.COM'
        password = 'teste123'
        nome = 'usuario 123'
        usuario = get_user_model().objects.create_user(
            email=email,
            password=password,
            nome=nome
        )

        self.assertEqual(usuario.email, email.lower())

    def test_novo_usuario_email_invalido(self):
        """Testa a criação de um usuário sem email, deve retornar erro"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='senha123',
                nome='nome do usuario'
            )

    def test_novo_usuario_sem_nome(self):
        """Testa a criação de um usuário sem nome, deve retornar erro"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='usuario@gmail.com',
                password='senha123',
                nome=''
            )
