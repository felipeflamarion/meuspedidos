# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal
from django.test import TestCase

from pedidos.tests.funcoes_auxiliares import populate_base_de_testes
from pedidos.models import PedidoModel, ProdutoModel, ItemModel


class ItemModelTeste(TestCase):
    def setUp(self):
        populate_base_de_testes()

    def teste_cadastro(self):
        produto = ProdutoModel.objects.get(pk=1)
        pedido = PedidoModel.objects.get(pk=1)

        item = ItemModel()
        item.pedido = pedido
        item.produto = produto
        item.preco = produto.preco_unitario
        item.quantidade = produto.multiplo
        item.save()
        self.assertEqual(ItemModel.objects.filter(id=item.id).exists(), True)

    def teste_rentabilidade(self):
        ''' Item com preço original 8.00 '''
        item = ItemModel.objects.get(pk=1)

        ''' rentabilidade ótima '''
        item.preco = Decimal.from_float(11.00)
        item.save()
        self.assertEqual(item.rentabilidade(), 2)
        item.preco = Decimal.from_float(8.01)
        item.save()
        self.assertEqual(item.rentabilidade(), 2)
        ''' rentabilidade boa '''
        item.preco = Decimal.from_float(8.00)
        item.save()
        self.assertEqual(item.rentabilidade(), 1)
        item.preco = Decimal.from_float(7.20)
        item.save()
        self.assertEqual(item.rentabilidade(), 1)
        ''' rentabilidade ruim '''
        item.preco = Decimal.from_float(7.19)
        item.save()
        self.assertEqual(item.rentabilidade(), 0)
        item.preco = Decimal.from_float(5.00)
        item.save()
        self.assertEqual(item.rentabilidade(), 0)

    def teste_item_get_or_none(self):
        item = ItemModel.get_or_none(100)
        self.assertEqual(item, None)
