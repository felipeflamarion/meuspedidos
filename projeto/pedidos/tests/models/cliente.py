# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from pedidos.models import ClienteModel


class ClienteModelTeste(TestCase):
    def teste_cadastro(self):
        cliente = ClienteModel()
        cliente.nome = 'Darth'
        cliente.sobrenome = 'Maul'
        cliente.save()
        self.assertEqual(ClienteModel.objects.filter(id=cliente.id).exists(), True)
