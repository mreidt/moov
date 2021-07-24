from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Empresa
from empresa.serializers import EmpresaSerializer


EMPRESA_URL = reverse('empresa:empresa-list')


def empresa_exemplo(**params):
    """Cria e retorna uma empresa de exemplo para testes"""
    defaults = {
        'nome': 'Empresa de Testes',
        'cnpj': '99.750.592/0001-26'
    }
    defaults.update(params)

    return Empresa.objects.create(**defaults)


def url_detalhe(id_empresa):
    """Retorna a URL dos detalhes de uma empresa"""
    return reverse('empresa:empresa-detail', args=[id_empresa])


class PublicEmpresaApiTests(TestCase):
    """Testa acesso sem autenticação às informações das empresas"""

    def setUp(self):
        self.client = APIClient()

    def test_autenticacao_necessaria(self):
        """Testa que a autenticação é necessária para acessar o endpoint"""
        res = self.client.get(EMPRESA_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEmpresaApiTests(TestCase):
    """Testa acesso autenticado à API das empresas"""

    def setUp(self):
        self.client = APIClient()
        self.usuario = get_user_model().objects.create_user(
            'teste_usuario@gmail.com',
            'senha123'
        )
        self.client.force_authenticate(self.usuario)

    def test_lista_empresas(self):
        """Testa endpoint de listar empresas"""
        empresa_exemplo()
        empresa_exemplo(nome='Empresa de testes 2', cnpj='18.754.544/0001-04')
        empresa_exemplo(nome='Empresa de testes 3', cnpj='08.607.145/0001-67')

        res = self.client.get(EMPRESA_URL)

        empresas = Empresa.objects.all()
        serializer = EmpresaSerializer(empresas, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_criar_empresa(self):
        """Testa a criação de uma empresa"""
        payload = {
            'nome': 'Binamik Tecnologia Limitada',
            'cnpj': '39417743000105'
        }
        res = self.client.post(EMPRESA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        empresa = Empresa.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(empresa, key))

    def test_atualizar_empresa_parcialmente_nome(self):
        """Testa a atualização do nome de uma empresa utilizando PATCH"""
        cnpj = '92.389.497/0001-08'
        empresa = empresa_exemplo(nome='qualquer', cnpj=cnpj)

        payload = {'nome': 'Nome alterado'}
        url = url_detalhe(empresa.id)
        self.client.patch(url, payload)

        empresa.refresh_from_db()
        self.assertEqual(empresa.nome, payload['nome'])
        self.assertEqual(empresa.cnpj, cnpj)

    def test_atualizar_empresa_parcialmente_cnpj(self):
        """Testa a atualização do cnpj de uma empresa utilizando PATCH"""
        nome = 'Nome de empresa ficticia'
        empresa = empresa_exemplo(nome=nome, cnpj='92.389.497/0001-08')

        payload = {'cnpj': '94.243.181/0001-20'}
        url = url_detalhe(empresa.id)
        self.client.patch(url, payload)

        empresa.refresh_from_db()
        self.assertEqual(empresa.nome, nome)
        self.assertEqual(empresa.cnpj, payload['cnpj'])

    def test_atualizar_empresa_completamente(self):
        """Testa a atualização completa de uma empresa utilizando PUT"""
        empresa = empresa_exemplo(nome='qualquer', cnpj='94.403.936/0001-07')
        payload = {'nome': 'Novo nome empresa', 'cnpj': '17.939.227/0001-08'}

        url = url_detalhe(empresa.id)
        self.client.put(url, payload)

        empresa.refresh_from_db()
        self.assertEqual(empresa.nome, payload['nome'])
        self.assertEqual(empresa.cnpj, payload['cnpj'])

    def test_cnpj_vazio(self):
        """Testa que um CNPJ vazio retorna erro"""
        payload = {
            'nome': 'Binamik Tecnologia Limitada',
            'cnpj': ''
        }
        res = self.client.post(EMPRESA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cnpj_invalido(self):
        """Testa que um CNPJ inválido retorna erro"""
        payload = {
            'nome': 'Binamik Tecnologia Limitada',
            'cnpj': '1'
        }
        res = self.client.post(EMPRESA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nome_vazio(self):
        """Testa que um nome vazio retorna erro"""
        payload = {
            'nome': '',
            'cnpj': '00.000.000/0001-00'
        }
        res = self.client.post(EMPRESA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cnpj_repetido(self):
        """Testa que um CNPJ deva ser único"""
        empresa_exemplo(nome='qualquer', cnpj='00.000.000/0001-00')

        payload = {
            'nome': '',
            'cnpj': '00.000.000/0001-00'
        }
        res = self.client.post(EMPRESA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
