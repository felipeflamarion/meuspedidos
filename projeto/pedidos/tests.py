# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from pedidos.models import *
from decimal import Decimal
from pedidos.views import *
from django.core.urlresolvers import reverse


# Create your tests here.

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
    def setUp(self):
        self.factory = RequestFactory()

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
        response = self.client.get(reverse('lista_pedidos'))
        self.assertEqual(response.status_code, 200)

    def teste_cancelar_pedido(self):
        cliente = ClienteModel(nome='Lando', sobrenome='Calrissian')
        cliente.save()
        pedido = PedidoModel(cliente=cliente)
        pedido.save()

        request = self.factory.get(reverse('index'))
        ''' Cancelar pedido com ID válido '''
        request.session = {'pedido': pedido.id}
        response = PedidoView.Cancelar(request=request)
        self.assertEqual(response.status_code, 302)
        ''' Cancelar pedido com ID inválido '''
        request.session = {'pedido': 1000}
        response = PedidoView.Cancelar(request=request)
        self.assertEqual(response.status_code, 404)

    def teste_finalizar_pedido(self):
        cliente = ClienteModel(nome='Lando', sobrenome='Calrissian')
        cliente.save()
        pedido = PedidoModel(cliente=cliente)
        pedido.save()

        request = self.factory.get(reverse('index'))
        ''' Finalizar pedido com ID válido '''
        request.session = {'pedido': pedido.id}
        response = PedidoView.Finalizar(request=request)
        self.assertEqual(response.status_code, 200)
        ''' Finalizar pedido com ID inválido '''
        request.session = {'pedido': 1000}
        response = PedidoView.Finalizar(request=request)
        self.assertEqual(response.status_code, 404)

    def teste_visualizar_pedido(self):
        cliente = ClienteModel(nome='Lando', sobrenome='Calrissian')
        cliente.save()
        pedido = PedidoModel(cliente=cliente)
        pedido.save()

        ''' Visualizar pedido com ID válido '''
        response = self.client.get(reverse('visualizar_pedido', kwargs={'id_pedido': pedido.id}))
        self.assertEqual(response.status_code, 200)
        ''' Visualizar pedido com ID inválido '''
        response = self.client.get(reverse('visualizar_pedido', kwargs={'id_pedido': 1000}))
        self.assertEqual(response.status_code, 404)

    def teste_valor_total_pedido(self):
        cliente = ClienteModel(nome='Lando', sobrenome='Calrissian')
        cliente.save()
        pedido = PedidoModel(cliente=cliente)
        pedido.save()
        produto1 = ProdutoModel(nome='Capacete Stormtrooper', preco_unitario=Decimal.from_float(1000.00))
        produto1.save()
        produto2 = ProdutoModel(nome='Blue Milk', preco_unitario=Decimal.from_float(10.00))
        produto2.save()

        ''' Itens em quantidade única de cada '''
        item1 = ItemModel(pedido=pedido, produto=produto1, preco=produto1.preco_unitario)
        item1.save()
        item2 = ItemModel(pedido=pedido, produto=produto2, preco=produto2.preco_unitario)
        item2.save()
        itens = ItemModel.objects.filter(pedido=pedido)
        self.assertEqual(PedidoView.valor_total(itens), Decimal.from_float(1010.00))
        ''' Com mais de uma unidade de um produto '''
        item2.quantidade = 10
        item2.save()
        itens = ItemModel.objects.filter(pedido=pedido)
        self.assertEqual(PedidoView.valor_total(itens), Decimal.from_float(1100.00))


class ProdutoViewTeste(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def teste_visualizar_produto(self):
        produto = ProdutoModel(nome='Capacete Stormtrooper', preco_unitario=Decimal.from_float(1000.00))
        produto.save()

        ''' Visualizar produto com ID inválido '''
        response = self.client.get(reverse('visualizar_produto', kwargs={'id_produto': produto.id}))
        self.assertEqual(response.status_code, 200)
        ''' Visualizar produto com ID inválido '''
        response = self.client.get(reverse('visualizar_produto', kwargs={'id_produto': 1000}))
        self.assertEqual(response.status_code, 404)

    def teste_listar_produto(self):
        response = self.client.get(reverse('lista_produtos'))
        self.assertEqual(response.status_code, 200)

    def teste_adicao_rapida_produto(self):
        cliente = ClienteModel(nome='Lando', sobrenome='Calrissian')
        cliente.save()
        pedido = PedidoModel(cliente=cliente)
        pedido.save()
        produto = ProdutoModel(nome='Capacete Stormtrooper', preco_unitario=Decimal.from_float(1000.00))
        produto.save()
        request = self.factory.get(reverse('index'))

        request.session = {}
        ''' Sem sessão ativa '''
        response = ProdutoView.AdicaoRapida(request=request, id_produto=produto.id)
        self.assertEqual(response.status_code, 200)

        request.session['pedido'] = pedido.id
        ''' Com sessão ativa e produto inválido '''
        response = ProdutoView.AdicaoRapida(request=request, id_produto=1000)
        self.assertEqual(response.status_code, 404)

        ''' Com sessão ativa e produto válido '''
        response = ProdutoView.AdicaoRapida(request=request, id_produto=produto.id)
        self.assertEqual(response.status_code, 302)


class ItemViewTeste(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def teste_novo_item(self):
        cliente = ClienteModel(nome='Lando', sobrenome='Calrissian')
        cliente.save()
        pedido = PedidoModel(cliente=cliente)
        pedido.save()
        produto = ProdutoModel(nome='Blue Milk', preco_unitario=Decimal.from_float(10.00), multiplo=5)
        produto.save()

        ''' Sem pedido ativo '''
        request = self.factory.get(reverse('index'))
        request.session = {}
        response = self.client.post(reverse('novo_item'), {'produto': produto.id, 'preco': Decimal.from_float(12.00), 'multiplo': 5})
        self.assertEqual(response.status_code, 200)

    def teste_editar_item(self):
        pass

    def teste_visualizar_item(self):
        pass

    def teste_excluir(self):
        cliente = ClienteModel(nome='Lando', sobrenome='Calrissian')
        cliente.save()
        pedido = PedidoModel(cliente=cliente)
        pedido.save()
        produto = ProdutoModel(nome='Blue Milk', preco_unitario=Decimal.from_float(10.00), multiplo=5)
        produto.save()
        item = ItemModel(pedido=pedido, produto=produto, quantidade=produto.multiplo, preco=produto.preco_unitario)
        item.save()
        request = self.factory.get(reverse('index'))

        ''' Exclusão de item com ID válido '''
        response = ItemView.Excluir(request=request, id_item=item.id)
        self.assertEqual(response.status_code, 302)
        ''' Exclusão de item com ID inválido '''
        response = ItemView.Excluir(request=request, id_item=1000)
        self.assertEqual(response.status_code, 404)
