# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pedidos.models import ProdutoModel
from decimal import Decimal


class ProdutoModelTeste(TestCase):
    def teste_multiplo_padrao(self):
        produto = ProdutoModel(nome='Blue Milk', preco_unitario=Decimal.from_float(10.00))
        produto.save()
        self.assertEqual(produto.multiplo, 1)
