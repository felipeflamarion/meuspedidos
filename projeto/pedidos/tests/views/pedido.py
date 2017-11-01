# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pedidos.tests.funcoes_auxiliares import *
from pedidos.views import PedidoView


class PedidoViewTeste(TestCase):
    def setUp(self):
        populate_base_de_testes()

    def teste_cadastro_pedido(self):
        ''' Sucesso: dados válidos '''
        response = self.client.post(reverse('novo_pedido'), {'cliente': 1})
        self.assertEqual(response.status_code, 302)
        ''' Falhou: dados inválidos '''
        response = self.client.get(reverse('novo_pedido'))
        self.assertEqual(response.status_code, 200)

    def teste_continuar_pedido(self):
        ''' Sucesso: ID válido '''
        response = self.client.get(reverse('continuar_pedido', kwargs={'id_pedido': 1}))
        self.assertEqual(response.status_code, 302)
        ''' Falhou: ID inválido '''
        response = self.client.get(reverse('continuar_pedido', kwargs={'id_pedido': 100}))
        self.assertEqual(response.status_code, 404)

    def teste_listar_pedidos(self):
        response = self.client.get(reverse('lista_pedidos'))
        self.assertEqual(response.status_code, 200)

    def teste_cancelar_pedido(self):
        ''' Sucesso: pedido cancelado '''
        request = get_sessao_pedido_generica(1)
        response = PedidoView.Cancelar(request=request)
        self.assertEqual(response.status_code, 302)
        ''' Falhou: pedido inválido '''
        request = get_sessao_pedido_generica(100)
        response = PedidoView.Cancelar(request=request)
        self.assertEqual(response.status_code, 404)

    def teste_finalizar_pedido(self):
        ''' Finalizar pedido com ID válido '''
        request = get_sessao_pedido_generica(1)
        response = PedidoView.Finalizar(request=request)
        self.assertEqual(response.status_code, 302)
        ''' Finalizar pedido com ID válido mas sem itens'''
        request = get_sessao_pedido_generica(2)
        response = PedidoView.Finalizar(request=request)
        self.assertEqual(response.status_code, 200)
        ''' Finalizar pedido com ID inválido '''
        request = get_sessao_pedido_generica(100)
        response = PedidoView.Finalizar(request=request)
        self.assertEqual(response.status_code, 404)

    def teste_visualizar_pedido(self):
        ''' Sucesso: ID válido '''
        response = self.client.get(reverse('visualizar_pedido', kwargs={'id_pedido': 1}))
        self.assertEqual(response.status_code, 200)
        ''' Falhou: ID inválido '''
        response = self.client.get(reverse('visualizar_pedido', kwargs={'id_pedido': 1000}))
        self.assertEqual(response.status_code, 404)

    def teste_valor_total_pedido(self):
        itens = ItemModel.objects.filter(pedido_id=1)
        valor_total = PedidoView.get_valor_total_pedido(itens)
        self.assertEqual(valor_total, Decimal.from_float(430120.00))
        itens = ItemModel.objects.filter(pedido_id=2)
        valor_total = PedidoView.get_valor_total_pedido(itens)
        self.assertEqual(valor_total, Decimal.from_float(0))
        itens = ItemModel.objects.filter(pedido_id=3)
        valor_total = PedidoView.get_valor_total_pedido(itens)
        self.assertEqual(valor_total, Decimal.from_float(5890.00))
        itens = ItemModel.objects.filter(pedido_id=4)
        valor_total = PedidoView.get_valor_total_pedido(itens)
        self.assertEqual(valor_total, Decimal.from_float(550000.00))
