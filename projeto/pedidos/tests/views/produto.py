# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pedidos.tests.funcoes_auxiliares import *
from pedidos.views import PedidoView, ProdutoView


class ProdutoViewTeste(TestCase):
    def setUp(self):
        populate_base_de_testes()

    def teste_visualizar_produto(self):
        ''' Visualizar produto com ID inválido '''
        response = self.client.get(reverse('visualizar_produto', kwargs={'id_produto': 1}))
        self.assertEqual(response.status_code, 200)
        ''' Visualizar produto com ID inválido '''
        response = self.client.get(reverse('visualizar_produto', kwargs={'id_produto': 100}))
        self.assertEqual(response.status_code, 404)

    def teste_listar_produto(self):
        response = self.client.get(reverse('lista_produtos'))
        self.assertEqual(response.status_code, 200)

    def teste_adicao_rapida_produto(self):
        ''' Sem sessão ativa '''
        factory = RequestFactory()
        request = factory.get(reverse('index'))
        request.session = {}
        response = ProdutoView.AdicaoRapida(request=request, id_produto=1)
        self.assertEqual(response.status_code, 200)
        ''' Com sessão ativa e produto inválido '''
        request = get_sessao_pedido_generica(1)
        response = ProdutoView.AdicaoRapida(request=request, id_produto=1000)
        self.assertEqual(response.status_code, 404)
        ''' Sessão ativa e produto válido '''
        request = get_sessao_pedido_generica(1)
        response = ProdutoView.AdicaoRapida(request=request, id_produto=1)
        self.assertEqual(response.status_code, 302)
