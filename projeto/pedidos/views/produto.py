# coding:utf-8
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from pedidos.models import ProdutoModel, ItemModel
from pedidos.views.functions import SessaoPedido
from pedidos.forms import ItemForm


class ProdutoView(View):
    @classmethod
    def Visualizar(self, request, id_produto=None):
        context_dict = {}
        produto = ProdutoModel.get_or_none(id=id_produto)
        if produto:
            pedido_ativo = SessaoPedido(request=request).get_objeto_pedido()
            if pedido_ativo:
                if produto in pedido_ativo.itens.all():
                    context_dict['item'] = ItemModel.objects.get(produto=produto, pedido=pedido_ativo)
            context_dict['produto'] = produto
            context_dict['form'] = ItemForm(preco=produto.preco_unitario, quantidade=produto.multiplo)
            context_dict['pedido_ativo'] = pedido_ativo
            context_dict['mensagem'] = self.get_produto_mensagem(request=request)
            return render(request, 'pedidos/visualizar_produto.html', context_dict)
        else:
            return HttpResponseNotFound('<h1>404</h1><p>Produto %s não existe!' % id_produto)

    @classmethod
    def Listar(self, request):
        context_dict = {}
        produtos = ProdutoModel.objects.all().order_by('nome')
        context_dict['produtos'] = produtos
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        context_dict['mensagem'] = self.get_produto_mensagem(request=request)
        return render(request, 'pedidos/lista_produtos.html', context_dict)

    @classmethod
    def AdicaoRapida(self, request, id_produto):
        # TODO refatorar esta view
        context_dict = {}
        try:
            produto = ProdutoModel.objects.get(pk=id_produto)
        except ProdutoModel.DoesNotExist:
            return HttpResponseNotFound('<h1>404</h1><p>Produto %s não existe!' % id_produto)

        pedido_ativo = SessaoPedido(request=request).get_objeto_pedido()
        if produto and pedido_ativo:
            if produto in pedido_ativo.itens.all():
                item = ItemModel.objects.get(produto=produto, pedido=pedido_ativo)
                item.quantidade += produto.multiplo
            else:
                item = ItemModel()
                item.produto = produto
                item.pedido = pedido_ativo
                item.preco = produto.preco_unitario
                item.quantidade = produto.multiplo
            item.save()
            return HttpResponseRedirect(urlresolvers.reverse('lista_produtos') + '?adicionado=True')
        else:
            mensagem = {'codigo': False, 'texto': 'Não foi possível adicionar o item ao pedido!'}

        context_dict['produto'] = produto
        context_dict['form'] = ItemForm(preco=produto.preco_unitario, quantidade=produto.multiplo)
        context_dict['pedido_ativo'] = pedido_ativo
        context_dict['mensagem'] = mensagem
        return render(request, 'pedidos/visualizar_produto.html', context_dict)

    def get_produto_mensagem(request):
        if request.GET.get('adicionado') == 'True':
            return {'codigo': True, 'texto': 'Item adicionado ao pedido!'}
        elif request.GET.get('removido') == 'True':
            return {'codigo': True, 'texto': 'Item removido do pedido!'}
        else:
            return None
