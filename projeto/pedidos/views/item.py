# coding:utf-8
from django.core import urlresolvers
from django.shortcuts import render, HttpResponseRedirect
from django.views import View

from pedidos.models import ProdutoModel, ItemModel
from pedidos.views.functions import SessaoPedido
from pedidos.forms import ItemForm


class ItemView(View):

    def post(self, request):
        context_dict = {}
        form = ItemForm(data=request.POST)
        produto = ProdutoModel.objects.get(pk=request.POST.get('produto'))
        pedido_ativo = SessaoPedido(request=request).get_objeto_pedido()

        if form.is_valid() and produto:
            item = form.save(commit=False)
            item.pedido = pedido_ativo
            item.produto = produto
            item.save()
            mensagem = {'codigo': True, 'texto': 'Item adicionado ao pedido!'}
        else:
            mensagem = {'codigo': False, 'texto': 'Não foi possível adicionar o item!'}

        context_dict['form'] = form
        context_dict['produto'] = produto
        context_dict['pedido_ativo'] = pedido_ativo
        context_dict['mensagem'] = mensagem
        return render(request, 'pedidos/visualizar_produto.html', context_dict)

    @classmethod
    def Excluir(self, request, id_item):
        context_dict = {}
        item = ItemModel.objects.get(pk=id_item)
        if not item.pedido.finalizado:
            item.delete()
            return HttpResponseRedirect(urlresolvers.reverse('visualizar_pedido', kwargs={'id_pedido': item.pedido.id}))
        else:
            mensagem = {'codigo': False, 'texto': 'Não é possível excluir itens de um pedido finalizado! Reabra o pedido para excluir!'}
        print(mensagem)
        # context_dict['mensagem'] = mensagem
        # context_dict['produto'] = item.produto
        # context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        # return render(request, 'pedidos/visualizar_produto.html', context_dict)
        return HttpResponseRedirect(urlresolvers.reverse('index'))

    @classmethod
    def Visualizar(self, request, id_item):
        context_dict = {}
        item = ItemModel.objects.get(pk=id_item)
        context_dict['item'] = item
        context_dict['item_form'] = ItemForm(instance=item, preco=item.preco, quantidade=item.quantidade)
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        return render(request, 'pedidos/visualizar_item.html', context_dict)

    @classmethod
    def Editar(self, request, id_item):
        context_dict = {}
        item = ItemModel.objects.get(pk=id_item)
        item_form = ItemForm(instance=item, data=request.POST)
        pedido_ativo = SessaoPedido(request=request).get_objeto_pedido()

        if item_form.is_valid():
            if not item.pedido.finalizado:
                item_form.save()
                mensagem = {'codigo': True, 'texto': 'Item editado!'}
            else:
                mensagem = {'codigo': False, 'texto': 'Não é permitido editar itens de pedidos finalizados! Reabra o pedido para editar!'}
        else:
            mensagem = {'codigo': False, 'texto': 'Não foi possível editar o item!'}

        context_dict['item'] = item
        context_dict['pedido_ativo'] = pedido_ativo
        context_dict['mensagem'] = mensagem
        context_dict['item_form'] = item_form
        return render(request, 'pedidos/visualizar_item.html', context_dict)