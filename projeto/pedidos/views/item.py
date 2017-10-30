# coding:utf-8
from django.core import urlresolvers
from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponseRedirect
from django.views import View

from pedidos.models import ProdutoModel, ItemModel
from pedidos.views.functions import SessaoPedido
from pedidos.forms import ItemForm


class ItemView(View):
    def post(self, request):
        context_dict = {}
        form = ItemForm(data=request.POST)
        try:
            produto = ProdutoModel.objects.get(pk=request.POST.get('produto'))
        except ProdutoModel.DoesNotExist:
            return HttpResponseRedirect('<h1>404</h1><p>Produto %s não existe!' % request.POST.get('produto'))

        pedido_ativo = SessaoPedido(request=request).get_objeto_pedido()

        if form.is_valid() and produto:
            item = form.save(commit=False)
            if item.quantidade % produto.multiplo == 0:
                item.pedido = pedido_ativo
                item.produto = produto
                item.save()
                return HttpResponseRedirect(
                    urlresolvers.reverse('visualizar_produto', kwargs={'id_produto': produto.id}) + '?adicionado=True')
            else:
                mensagem = {'codigo': False,
                            'texto': 'Quantidade inválida (deve-se respeitar o valor múltiplo de venda do produto: %d)' % produto.multiplo}
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
        try:
            item = ItemModel.objects.get(pk=id_item)
        except ItemModel.DoesNotExist:
            return HttpResponseNotFound('<h1>404</h1><p>Item %s não existe!' % id_item)

        if not item.pedido.finalizado:
            item.delete()
            if request.GET.get('destino') == 'pedido':
                return HttpResponseRedirect(
                    urlresolvers.reverse('visualizar_pedido', kwargs={'id_pedido': item.pedido.id}) + '?removido=True')
            return HttpResponseRedirect(
                urlresolvers.reverse('visualizar_produto', kwargs={'id_produto': item.produto.id}) + '?removido=True')
        else:
            context_dict['mensagem'] = {'codigo': False,
                                        'texto': 'Não é possível excluir itens de um pedido finalizado! Reabra o pedido para excluir!'}
        context_dict['pedido'] = item.pedido
        context_dict['itens'] = ItemModel.objects.filter(pedido=item.pedido)
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        return render(request, 'pedidos/visualizar_pedido.html', context_dict)

    @classmethod
    def Visualizar(self, request, id_item):
        context_dict = {}
        try:
            item = ItemModel.objects.get(pk=id_item)
        except ItemModel.DoesNotExist:
            return HttpResponseNotFound('<h1>404</h1><p>Item %s não existe!' % id_item)
        context_dict['item'] = item
        context_dict['form'] = ItemForm(instance=item, preco=item.preco, quantidade=item.quantidade)
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        return render(request, 'pedidos/visualizar_item.html', context_dict)

    @classmethod
    def Editar(self, request, id_item):
        if request.method == 'GET':
            return HttpResponseRedirect(urlresolvers.reverse('visualizar_item', kwargs={'id_item': id_item}))
        context_dict = {}
        try:
            item = ItemModel.objects.get(pk=id_item)
        except ItemModel.DoesNotExist:
            return HttpResponseNotFound('<h1>404</h1><p>Item %s não existe!' % id_item)
        form = ItemForm(instance=item, data=request.POST)
        pedido_ativo = SessaoPedido(request=request).get_objeto_pedido()

        if form.is_valid():
            if not item.pedido.finalizado:
                if item.quantidade % item.produto.multiplo == 0:
                    form.save()
                    mensagem = {'codigo': True, 'texto': 'Item editado!'}
                else:
                    mensagem = {'codigo': False,
                                'texto': 'Quantidade inválida (deve-se respeitar o valor múltiplo de venda do produto: %d)' % item.produto.multiplo}
            else:
                mensagem = {'codigo': False,
                            'texto': 'Não é permitido editar itens de pedidos finalizados! Reabra o pedido para editar!'}
        else:
            mensagem = {'codigo': False, 'texto': 'Não foi possível editar o item!'}

        context_dict['item'] = item
        context_dict['pedido_ativo'] = pedido_ativo
        context_dict['mensagem'] = mensagem
        context_dict['form'] = form
        return render(request, 'pedidos/visualizar_item.html', context_dict)
