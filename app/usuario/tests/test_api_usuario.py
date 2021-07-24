from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


URL_CRIAR_USUARIO = reverse('usuario:criar')
URL_TOKEN = reverse('usuario:token')
URL_EU = reverse('usuario:eu')


def cria_usuario(**params):
    return get_user_model().objects.create_user(**params)


class PuclicUsuarioApiTests(TestCase):
    """Testa a API de usuários (pública)"""

    def setUp(self):
        self.client = APIClient()

    def test_criar_usuario_valido(self):
        """Testa a criação de um usuário com sucesso"""
        payload = {
            'email': 'usuario@email.com',
            'password': 'senha123',
            'nome': 'Algum nome'
        }
        res = self.client.post(URL_CRIAR_USUARIO, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        usuario = get_user_model().objects.get(**res.data)
        self.assertTrue(usuario.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_usuario_ja_existe(self):
        """Testa que a criação de um usuário já existente falha"""
        payload = {
            'email': 'usuario@email.com',
            'password': 'senha123',
            'nome': 'Algum nome'
        }
        cria_usuario(**payload)

        res = self.client.post(URL_CRIAR_USUARIO, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_senha_muito_curta(self):
        """Testa que a senha tenha pelo menos 8 caracteres"""
        payload = {
            'email': 'usuario@email.com',
            'password': '12345',
            'nome': 'Algum nome'
        }
        res = self.client.post(URL_CRIAR_USUARIO, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        existe_usuario = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(existe_usuario)

    def test_cria_token_para_usuario(self):
        """Testa que um token é criado para o usuário"""
        payload = {
            'email': 'usuario@email.com',
            'password': '12345678',
            'nome': 'Algum nome'
        }
        cria_usuario(**payload)
        res = self.client.post(URL_TOKEN, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_cria_token_credenciais_invalidas(self):
        """
        Testa que um token não é criado se credenciais inválidas
        forem utilizadas.
        """
        cria_usuario(
            email='usuario@email.com',
            password='12345678',
            nome='Algum nome'
        )
        payload = {'email': 'usuario@email.com', 'password': 'errado'}
        res = self.client.post(URL_TOKEN, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_token_usuario_inexistente(self):
        payload = {
            'email': 'usuario@email.com',
            'password': '12345678',
            'nome': 'Algum nome'
        }
        res = self.client.post(URL_TOKEN, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_token_sem_senha(self):
        res = self.client.post(
            URL_TOKEN, {
                'email': 'usuario@email.com',
                'password': ''
            }
        )
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_token_sem_email(self):
        res = self.client.post(
            URL_TOKEN, {
                'email': '',
                'password': '12345678'
            }
        )
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_autenticacao_detalhes_usuario(self):
        """Testa que é exigida autenticação ao buscar detalhes dos usuários"""
        res = self.client.get(URL_EU)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUsuarioApiTests(TestCase):
    """Testa requests de API que requerem autenticação"""

    def setUp(self):
        self.usuario = cria_usuario(
            email='usuario@email.com',
            password='12345678',
            nome='Nome de usuario'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.usuario)

    def test_busca_perfil_com_sucesso(self):
        """Testa busca de perfil do usuário autenticado"""
        res = self.client.get(URL_EU)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'nome': self.usuario.nome,
            'email': self.usuario.email
        })

    def test_post_nao_permitido_na_pagina_pessoal(self):
        """Testa o método POST na url do perfil do usuário - /eu"""
        res = self.client.post(URL_EU, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_atualizar_perfil_usuario(self):
        """Testa a atualização do perfil do usuário autenticado"""
        payload = {
            'nome': 'Novo nome',
            'password': 'novasenha123'
        }

        res = self.client.patch(URL_EU, payload)

        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nome, payload['nome'])
        self.assertTrue(self.usuario.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
