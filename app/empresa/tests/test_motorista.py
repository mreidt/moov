from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Empresa, Motorista
from empresa.serializers import MotoristaSerializer

MOTORISTA_URL = reverse('empresa:motorista-list')


def empresa_exemplo(**params):
    """Cria e retorna uma empresa de exemplo para testes"""
    defaults = {
        'nome': 'Empresa de Testes',
        'cnpj': '99.750.592/0001-26'
    }
    defaults.update(params)

    return Empresa.objects.create(**defaults)


def motorista_exemplo(empresa, **params):
    """Cria e retorna um motorista de exemplo para testes"""
    defaults = {
        'nome': 'Motorista 1',
        'cnh': '97270429357',
        'empresa': empresa
    }
    defaults.update(params)

    return Motorista.objects.create(**defaults)


def url_detalhe(id_motorista):
    """Retorna a URL dos detalhes de um motorista"""
    return reverse('empresa:motorista-detail', args=[id_motorista])


class PublicMotoristaApiTests(TestCase):
    """Testa acesso sem autenticação às informações de um motorista"""

    def setUp(self):
        self.client = APIClient()

    def test_autenticacao_necessaria(self):
        """Testa que a autenticação é necessária para acessar o endpoint"""
        res = self.client.get(MOTORISTA_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMotoristaApiTests(TestCase):
    """Testa acesso autenticado à API dos motoristas"""

    def setUp(self):
        self.client = APIClient()
        self.usuario = get_user_model().objects.create_user(
            'teste_usuario@gmail.com',
            'senha123'
        )
        self.client.force_authenticate(self.usuario)

    def test_lista_motoristas(self):
        """Testa endpoint de listar motoristas"""
        empresa = empresa_exemplo()
        motorista_exemplo(empresa=empresa)
        motorista_exemplo(
            nome='Motorista 2',
            cnh='33526650805',
            empresa=empresa
        )
        motorista_exemplo(
            nome='Motorista 3',
            cnh='58379537298',
            empresa=empresa
        )

        res = self.client.get(MOTORISTA_URL)

        motoristas = Motorista.objects.all()
        serializer = MotoristaSerializer(motoristas, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_criar_motorista(self):
        """Testa a criação de um motorista"""
        payload = {
            'nome': 'Motorista Aleatório',
            'cnh': '19143851779',
            'empresa': empresa_exemplo().id
        }
        res = self.client.post(MOTORISTA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        motorista = Motorista.objects.get(id=res.data['id'])
        for key in payload.keys():
            if key == 'empresa':
                self.assertEqual(payload[key], getattr(motorista, key).id)
            else:
                self.assertEqual(payload[key], getattr(motorista, key))

    def test_atualizar_motorista_parcialmente_nome(self):
        """Testa a atualização do nome do motorista utilizando PATCH"""
        cnh = '92872937116'
        empresa = empresa_exemplo()
        motorista = motorista_exemplo(
            nome='motorista 999',
            cnh=cnh,
            empresa=empresa
        )

        payload = {'nome': 'Nome do novo motorista'}
        url = url_detalhe(motorista.id)
        self.client.patch(url, payload)

        motorista.refresh_from_db()
        self.assertEqual(motorista.nome, payload['nome'])
        self.assertEqual(motorista.cnh, cnh)
        self.assertEqual(motorista.empresa.id, empresa.id)

    def test_atualizar_motorista_parcialmente_cnh(self):
        """Testa a atualização da CNH do motorista utilizando PATCH"""
        nome = 'motorista cnh alterada'
        empresa = empresa_exemplo()
        motorista = motorista_exemplo(
            nome=nome,
            cnh='07030185351',
            empresa=empresa
        )

        payload = {'cnh': '84423489969'}
        url = url_detalhe(motorista.id)
        self.client.patch(url, payload)

        motorista.refresh_from_db()
        self.assertEqual(motorista.nome, nome)
        self.assertEqual(motorista.cnh, payload['cnh'])
        self.assertEqual(motorista.empresa.id, empresa.id)

    def test_atualizar_motorista_parcialmente_empresa(self):
        """Testa a atualização da empresa do motorista utilizando PATCH"""
        nome = 'motorista empresa alterada'
        cnh = '92872937116'
        motorista = motorista_exemplo(
            nome=nome,
            cnh=cnh,
            empresa=empresa_exemplo()
        )

        empresa = Empresa.objects.create(
            nome='Empresa Nova',
            cnpj='07.831.181/0001-47'
        )
        payload = {'empresa': empresa.id}
        url = url_detalhe(motorista.id)
        self.client.patch(url, payload)

        motorista.refresh_from_db()
        self.assertEqual(motorista.nome, nome)
        self.assertEqual(motorista.cnh, cnh)
        self.assertEqual(motorista.empresa, empresa)

    def test_atualizar_motorista_completamente(self):
        """Testa a atualização completa de um motorista utilizando PUT"""
        motorista = motorista_exemplo(empresa=empresa_exemplo())
        empresa = Empresa.objects.create(
            nome='Empresa Nova',
            cnpj='07.831.181/0001-47'
        )
        payload = {
            'nome': 'Motorista com novo nome',
            'cnh': '11729993383',
            'empresa': empresa.id
        }

        url = url_detalhe(motorista.id)
        self.client.put(url, payload)

        motorista.refresh_from_db()
        self.assertEqual(motorista.nome, payload['nome'])
        self.assertEqual(motorista.cnh, payload['cnh'])
        self.assertEqual(motorista.empresa.id, payload['empresa'])

    def test_cnh_vazia(self):
        """Testa que um motorista sem CNH retorna erro"""
        payload = {
            'nome': 'Motorista sem CNH',
            'cnh': '',
            'empresa': empresa_exemplo()
        }
        res = self.client.post(MOTORISTA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nome_vazio(self):
        """Testa que um motorista sem nome retorna erro"""
        payload = {
            'nome': '',
            'cnh': '11729993383',
            'empresa': empresa_exemplo()
        }
        res = self.client.post(MOTORISTA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empresa_vazia(self):
        """Testa que um motorista sem empresa retorna erro"""
        payload = {
            'nome': 'Motorista sem empresa',
            'cnh': '11729993383',
            'empresa': ''
        }
        res = self.client.post(MOTORISTA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cnh_repetida(self):
        """Testa que o campo CNH é único na base"""
        cnh = '49597581477'
        empresa = empresa_exemplo()
        motorista_exemplo(
            nome='motorista 1',
            cnh=cnh,
            empresa=empresa
        )

        payload = {
            'nome': 'motorista 2',
            'cnh': cnh,
            'empresa': empresa
        }
        res = self.client.post(MOTORISTA_URL, payload)

        motoristas = Motorista.objects.all()
        self.assertEqual(len(motoristas), 1)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cnh_invalida(self):
        """Testa que uma CNH inválida retorna erro"""
        payload = {
            'nome': 'motorista cnh invalida',
            'cnh': '1',
            'empresa': empresa_exemplo()
        }
        res = self.client.post(MOTORISTA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
