# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pedidos.models import ProdutoModel
from decimal import Decimal


class ProdutoModelTeste(TestCase):
    def teste_cadastro(self):
        produto = ProdutoModel()
        produto.nome = 'Hiperpropulsor'
        produto.preco_unitario = Decimal.from_float(25000)
        produto.multiplo = 1
        produto.save()
        self.assertEqual(ProdutoModel.objects.filter(id=produto.id).exists(), True)

    def teste_multiplo_padrao(self):
        produto = ProdutoModel(nome='Blue Milk', preco_unitario=Decimal.from_float(10.00))
        produto.save()
        self.assertEqual(produto.multiplo, 1)

    def teste_produto_get_or_none(self):
        produto = ProdutoModel.get_or_none(100)
        self.assertEqual(produto, None)
