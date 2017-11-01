# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from pedidos.models import *
from decimal import Decimal

def get_sessao_pedido_generica(id_pedido):
    factory = TestCase.factory = RequestFactory()
    request = factory.get(reverse('index'))
    request.session = {'pedido': id_pedido}
    return request

def populate_base_de_testes():
    clientes = [
        ClienteModel(id=1, nome='Leia', sobrenome='Organa'),
        ClienteModel(id=2, nome='Lando', sobrenome='Calrissian'),
        ClienteModel(id=3, nome='Padme', sobrenome='Amidala')
    ]
    __salvar_instancias(clientes)

    pedidos = [
        PedidoModel(id=1, cliente_id=1),
        PedidoModel(id=2, cliente_id=1),
        PedidoModel(id=3, cliente_id=2),
        PedidoModel(id=4, cliente_id=3)
    ]
    __salvar_instancias(pedidos)

    produtos = [
        ProdutoModel(id=1, nome='Blue Milk', preco_unitario=Decimal.from_float(8.00), multiplo=5),
        ProdutoModel(id=2, nome='Stormtrooper Armor', preco_unitario=Decimal.from_float(5000.00), multiplo=1),
        ProdutoModel(id=3, nome='Stormtrooper Helmet', preco_unitario=Decimal.from_float(1200.00), multiplo=1),
        ProdutoModel(id=4, nome='AT-AT Walker', preco_unitario=Decimal.from_float(100000.00), multiplo=1)
    ]
    __salvar_instancias(produtos)

    itens = [
        ItemModel(id=1, produto_id=1, pedido_id=1, preco=Decimal.from_float(8.00), quantidade=15),
        ItemModel(id=2, produto_id=2, pedido_id=1, preco=Decimal.from_float(5500.00), quantidade=50),
        ItemModel(id=3, produto_id=3, pedido_id=1, preco=Decimal.from_float(1200.00), quantidade=50),
        ItemModel(id=4, produto_id=4, pedido_id=1, preco=Decimal.from_float(95000.00), quantidade=1),
        ItemModel(id=5, produto_id=1, pedido_id=3, preco=Decimal.from_float(8.00), quantidade=5),
        ItemModel(id=6, produto_id=2, pedido_id=3, preco=Decimal.from_float(5000.00), quantidade=1),
        ItemModel(id=7, produto_id=3, pedido_id=3, preco=Decimal.from_float(850.00), quantidade=1),
        ItemModel(id=8, produto_id=4, pedido_id=4, preco=Decimal.from_float(110000.00), quantidade=5),
    ]
    __salvar_instancias(itens)


def __salvar_instancias(instancias):
    for instancia in instancias:
        instancia.save()