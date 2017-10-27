# coding:utf-8
from django.shortcuts import render
from django.views import View
from pedidos.models import ProdutoModel, ItemModel
from pedidos.views.functions import SessaoPedido
from pedidos.forms import ItemForm

class ProdutoView(View):

    @classmethod
    def Visualizar(self, request, id_produto=None):
        context_dict = {}
        produto = ProdutoModel.objects.get(pk=id_produto)
        context_dict['produto'] = produto
        context_dict['item_form'] = ItemForm(preco=produto.preco_unitario, quantidade=produto.multiplo)
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        return render(request, 'pedidos/visualizar_produto.html', context_dict)

    @classmethod
    def Listar(self, request):
        context_dict = {}
        produtos = ProdutoModel.objects.all()
        context_dict['produtos'] = produtos
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        return render(request, 'pedidos/lista_produtos.html', context_dict)

    @classmethod
    def AdicaoRapida(self, request, id_produto):
        context_dict = {}
        produto = ProdutoModel.objects.get(pk=id_produto)
        pedido = SessaoPedido(request=request).get_objeto_pedido()
        if produto and pedido:
            item = ItemModel()
            item.pedido = pedido
            item.produto = produto
            item.preco = produto.preco_unitario
            if produto.multiplo:
                item.quantidade = produto.multiplo
            item.save()
            mensagem = {'codigo': True, 'texto': 'Item adicionado ao pedido!'}
        else:
            mensagem = {'codigo': False, 'texto': 'Não foi possível adicionar o item ao pedido!'}

        produtos = ProdutoModel.objects.all()
        context_dict['produtos'] = produtos
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        context_dict['mensagem'] = mensagem
        return render(request, 'pedidos/lista_produtos.html', context_dict)