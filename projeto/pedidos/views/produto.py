# coding:utf-8
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from pedidos.models import ProdutoModel
from pedidos.views.functions import SessaoPedido
from pedidos.forms import ItemForm

class ProdutoView(View):

    @classmethod
    def Visualizar(self, request, id_produto=None):
        context_dict = {}
        context_dict['produto'] = ProdutoModel.objects.get(pk=id_produto)
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        return render(request, 'pedidos/visualizar_produto.html', context_dict)

    @classmethod
    def Listar(self, request):
        context_dict = {}
        produtos = ProdutoModel.objects.all()
        context_dict['produtos'] = produtos
        context_dict['item_form'] = ItemForm()
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        return render(request, 'pedidos/lista_produtos.html', context_dict)