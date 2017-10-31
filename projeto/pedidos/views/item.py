# coding:utf-8
from django.core import urlresolvers
from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponseRedirect
from django.views import View

from pedidos.models import ProdutoModel, ItemModel
from pedidos.views.functions import SessaoPedido, get_mensagem
from pedidos.forms import ItemForm


class ItemView(View):
    def post(self, request):
        context_dict = {}
        form = ItemForm(data=request.POST)
        produto = ProdutoModel.get_or_none(id=request.POST.get('produto'))
        if produto:
            pedido_ativo = SessaoPedido(request=request).get_objeto_pedido()
            if form.is_valid():
                item = form.save(commit=False)
                if item.quantidade % produto.multiplo == 0:
                    item.pedido = pedido_ativo
                    item.produto = produto
                    item.save()
                    return HttpResponseRedirect(urlresolvers.reverse('visualizar_produto', kwargs={
                        'id_produto': produto.id}) + '?adicionado=True')
                else:
                    context_dict['mensagem'] = get_mensagem('item', 'quantidade_invalida')
            else:
                context_dict['mensagem'] = get_mensagem('item', 'cadastro_falhou')
        else:
            return HttpResponseNotFound('<h1>404</h1><p>Produto %s não existe!' % request.POST.get('produto'))
        context_dict['form'] = form
        context_dict['produto'] = produto
        context_dict['pedido_ativo'] = pedido_ativo
        return render(request, 'pedidos/visualizar_produto.html', context_dict)

    @classmethod
    def Excluir(self, request, id_item):
        context_dict = {}
        item = ItemModel.get_or_none(id=id_item)
        if item:
            if not item.pedido.finalizado:
                item.delete()
                if request.GET.get('destino') == 'pedido':
                    return HttpResponseRedirect(
                        urlresolvers.reverse('visualizar_pedido',
                                             kwargs={'id_pedido': item.pedido.id}) + '?removido=True')
                return HttpResponseRedirect(
                    urlresolvers.reverse('visualizar_produto',
                                         kwargs={'id_produto': item.produto.id}) + '?removido=True')
            else:
                context_dict['mensagem'] = {'codigo': False,
                                            'texto': 'Não é possível excluir itens de um pedido finalizado! Reabra o pedido para excluir!'}
            context_dict['pedido'] = item.pedido
            context_dict['itens'] = ItemModel.objects.filter(pedido=item.pedido)
            context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
            return render(request, 'pedidos/visualizar_pedido.html', context_dict)
        else:
            return HttpResponseNotFound('<h1>404</h1><p>Item %s não existe!' % id_item)

    @classmethod
    def Visualizar(self, request, id_item):
        context_dict = {}
        item = ItemModel.get_or_none(id=id_item)
        if item:
            context_dict['item'] = item
            context_dict['form'] = ItemForm(instance=item, preco=item.preco, quantidade=item.quantidade)
            context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
            return render(request, 'pedidos/visualizar_item.html', context_dict)
        return HttpResponseNotFound('<h1>404</h1><p>Item %s não existe!' % id_item)

    @classmethod
    def Editar(self, request, id_item):
        if request.method == 'GET':
            return HttpResponseRedirect(urlresolvers.reverse('visualizar_item', kwargs={'id_item': id_item}))
        context_dict = {}
        item = ItemModel.get_or_none(id=id_item)
        if item:
            form = ItemForm(instance=item, data=request.POST)
            pedido_ativo = SessaoPedido(request=request).get_objeto_pedido()

            if form.is_valid():
                if not item.pedido.finalizado:
                    if item.quantidade % item.produto.multiplo == 0:
                        form.save()
                        context_dict['mensagem'] = get_mensagem('item', 'item_editado')
                    else:
                        context_dict['mensagem'] = get_mensagem('item', 'quantidade_invalida')
                else:
                    context_dict['mensagem'] = get_mensagem('item', 'pedido_nao_finalizado')
            else:
                context_dict['mensagem'] = get_mensagem('item', 'edicao_falhou')
            context_dict['item'] = item
            context_dict['pedido_ativo'] = pedido_ativo
            context_dict['form'] = form
            return render(request, 'pedidos/visualizar_item.html', context_dict)
        else:
            return HttpResponseNotFound('<h1>404</h1><p>Item %s não existe!' % id_item)
