# coding:utf-8
from django.core import urlresolvers
from django.shortcuts import render, HttpResponseRedirect
from django.views import View

from pedidos.models import ProdutoModel
from pedidos.views.functions import SessaoPedido
from pedidos.forms import ItemForm


class ItemView(View):

    def post(self, request):
        context_dict = {}
        form = ItemForm(data=request.POST)
        pedido = SessaoPedido(request=request)
        produto = self.get_produto(request.POST.get('produto'))

        if form.is_valid() and produto:
            item = form.save(commit=False)
            item.pedido = pedido.get_objeto_pedido()
            item.produto = produto
            item.save()
            mensagem = {'codigo': True, 'texto': 'Item adicionado ao pedido!'}
        else:
            mensagem = {'codigo': False, 'texto': 'Não foi possível adicionar o item!'}

        context_dict['produto'] = produto
        context_dict['pedido_ativo'] = pedido.get_objeto_pedido()
        context_dict['form'] = form
        context_dict['mensagem'] = mensagem
        return render(request, 'pedidos/produto.html', context_dict)

    def get_produto(self, id_produto):
        try:
            return ProdutoModel.objects.get(pk=id_produto)
        except:
            return None