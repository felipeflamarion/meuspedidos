# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pedidos.tests.funcoes_auxiliares import populate_base_de_testes
from pedidos.models import PedidoModel, ClienteModel


class PedidoModelTeste(TestCase):
    def setUp(self):
        populate_base_de_testes()

    def teste_cadastro(self):
        pedido = PedidoModel()
        pedido.cliente = ClienteModel.objects.get(pk=1)
        pedido.save()
        self.assertEqual(PedidoModel.objects.filter(id=pedido.id).exists(), True)

    def teste_estado_padrao(self):
        pedido = PedidoModel()
        pedido.cliente = ClienteModel.objects.get(pk=2)
        pedido.save()
        self.assertEqual(pedido.finalizado, False)

    def teste_pedido_get_or_none(self):
        pedido = PedidoModel.get_or_none(100)
        self.assertEqual(pedido, None)
