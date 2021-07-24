from rest_framework import serializers

from core.models import Empresa, Motorista

import re


class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para objetos do tipo empresa"""

    def validate(self, data):
        """Valida o CNPJ"""
        cnpj = data.get('cnpj', None)
        if not cnpj:
            return data
        cnpj = re.sub(r'\W+', '', cnpj)
        if not cnpj.isdigit:
            raise serializers.ValidationError(
                {'cnpj': 'CNPJ inválido!'})
        if len(cnpj) != 14:
            raise serializers.ValidationError(
                {'cnpj': 'CNPJ deve ter 14 dígitos!'})
        cnpj_int = map(int, cnpj[:-2])
        pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        resultado = sum(
            [digito * peso for digito, peso in zip(cnpj_int, pesos)]
        )
        digito1 = 0 if resultado % 11 < 2 else 11 - resultado % 11
        cnpj_int = map(int, cnpj[:-1])
        pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        resultado = sum(
            [digito * peso for digito, peso in zip(cnpj_int, pesos)]
        )
        digito2 = 0 if resultado % 11 < 2 else 11 - resultado % 11
        if int(cnpj[-2]) != digito1 or int(cnpj[-1]) != digito2:
            raise serializers.ValidationError(
                {'cnpj': 'Dígito verificador do CNPJ inválido!'})
        return data

    class Meta:
        model = Empresa
        fields = ('id', 'nome', 'cnpj')
        read_only_fields = ('id',)


class MotoristaSerializer(serializers.ModelSerializer):
    """Serializer para objetos do tipo motorista"""

    class Meta:
        model = Motorista
        fields = ('id', 'nome', 'cnh', 'empresa')
        read_only_fields = ('id',)
