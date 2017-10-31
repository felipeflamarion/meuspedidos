# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pedidos.models import *
from decimal import Decimal
from pedidos.views import *
from django.core.urlresolvers import reverse, NoReverseMatch

# Create your tests here.
from pedidos.views.functions import SessaoPedido


class ProdutoModelTeste(TestCase):
    def teste_multiplo_padrao(self):
        produto = ProdutoModel(nome='Blue Milk', preco_unitario=Decimal.from_float(10.00))
        produto.save()
        self.assertEqual(produto.multiplo, 1)


class PedidoModelTeste(TestCase):
    pass


class ItemModelTeste(TestCase):
    def teste_quantidade_padrao(self):
        cliente = ClienteModel(nome='Lando', sobrenome='Calrissian')
        cliente.save()
        pedido = PedidoModel(cliente=cliente)
        pedido.save()
        produto = ProdutoModel(nome='Capacete Stormtrooper', preco_unitario=Decimal.from_float(1000.00))
        produto.save()

        item = ItemModel(pedido=pedido, produto=produto, preco=produto.preco_unitario)
        item.save()
        self.assertEqual(item.quantidade, 1)

    def teste_rentabilidade(self):
        cliente = ClienteModel(nome='Lando', sobrenome='Calrissian')
        cliente.save()
        pedido = PedidoModel(cliente=cliente)
        pedido.save()
        produto = ProdutoModel(nome='Blue Milk', preco_unitario=Decimal.from_float(10.00), multiplo=5)
        produto.save()
        ''' rentabilidade ótima '''
        item = ItemModel(pedido=pedido, produto=produto, preco=Decimal.from_float(11.00), quantidade=5)
        item.save()
        self.assertEqual(item.rentabilidade(), 2)
        ''' rentabilidade boa '''
        item = ItemModel(pedido=pedido, produto=produto, preco=Decimal.from_float(10.00), quantidade=5)
        item.save()
        self.assertEqual(item.rentabilidade(), 1)
        ''' rentabilidade ruim '''
        item = ItemModel(pedido=pedido, produto=produto, preco=Decimal.from_float(5.00), quantidade=5)
        item.save()
        self.assertEqual(item.rentabilidade(), 0)


class IndexViewTeste(TestCase):
    def teste_funcionalidade_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class PedidoViewTeste(TestCase):
    def teste_cadastro_novo_pedido(self):
        response = self.client.get(reverse('novo_pedido'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('novo_pedido'), {'cliente': 1})
        self.assertEqual(response.status_code, 200)

    def teste_continuar_pedido(self):
        cliente = ClienteModel(nome='Lando', sobrenome='Calrissian')
        cliente.save()
        pedido = PedidoModel(cliente=cliente)
        pedido.save()
        ''' Continuar pedido com ID válido '''
        response = self.client.get(reverse('continuar_pedido', kwargs={'id_pedido': pedido.id}))
        self.assertEqual(response.status_code, 302)
        ''' Continuar pedido com ID inválido '''
        response = self.client.get(reverse('continuar_pedido', kwargs={'id_pedido': 9}))
        self.assertEqual(response.status_code, 404)

    def teste_listar_pedido(self):
        pass

    def teste_cancelar_pedido(self):
        pass

    def teste_finalizar_pedido(self):
        pass

    def teste_visualizar_pedido(self):
        pass

    def teste_valor_total_pedido(self):
        pass


class ProdutoViewTeste(TestCase):
    def teste_visualizar_produto(self):
        pass

    def teste_listar_produto(self):
        pass

    def teste_adicao_rapida_produto(self):
        pass


class ItemViewTeste(TestCase):
    def teste_novo_item(self):
        pass

    def teste_editar_item(self):
        pass

    def teste_visualizar_item(self):
        pass

    def teste_excluir(self):
        pass
