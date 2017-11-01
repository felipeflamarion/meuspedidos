# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from decimal import Decimal
from django.test import TestCase
from pedidos.tests.funcoes_auxiliares import get_sessao_pedido_generica, populate_base_de_testes
from pedidos.views import ItemView
from pedidos.models import PedidoModel


class ItemViewTeste(TestCase):
    def setUp(self):
        populate_base_de_testes()

    def teste_novo_item(self):
        ''' Sem sessão de pedido ativa '''
        response = self.client.post(reverse('novo_item'), {'produto': 1, 'preco': Decimal.from_float(9.00), 'multiplo': 15})
        self.assertEqual(response.status_code, 200)
        ''' Com sessão de pedido ativa '''
        response = self.client.post(reverse('novo_item'),{'produto': 10, 'preco': Decimal.from_float(9.00), 'multiplo': 15})
        self.assertEqual(response.status_code, 404)

    def teste_excluir_item(self):
        ''' Sucesso: item excluído '''
        request = get_sessao_pedido_generica(3)
        response = ItemView.Excluir(request=request, id_item=5)
        self.assertEqual(response.status_code, 302)
        ''' Falhou: ID inválido '''
        request = get_sessao_pedido_generica(3)
        response = ItemView.Excluir(request=request, id_item=100)
        self.assertEqual(response.status_code, 404)
        ''' Falhou: pedido finalizado não deve permitr remoção de itens '''
        pedido = PedidoModel.objects.get(pk=4)
        pedido.finalizado = True
        pedido.save()
        response = ItemView.Excluir(request=request, id_item=8)
        self.assertEqual(response.status_code, 200)

    def teste_visualizar_item(self):
        ''' Sucesso: item visualizado '''
        response = self.client.get(reverse('visualizar_item', kwargs={'id_item': 1}))
        self.assertEqual(response.status_code, 200)
        ''' Falhou: ID inválido '''
        response = self.client.get(reverse('visualizar_item', kwargs={'id_item': 100}))
        self.assertEqual(response.status_code, 404)

    def teste_editar_item(self):
        ''' Falhou: essa view só aceita método POST '''
        request = get_sessao_pedido_generica(1)
        response = ItemView.Editar(request=request, id_item=3)
        self.assertEqual(response.status_code, 302)
