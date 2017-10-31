# coding:utf-8
from django.core import urlresolvers
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from pedidos.forms import PedidoForm
from pedidos.models import PedidoModel, ItemModel
from pedidos.views.functions import SessaoPedido, get_mensagem


class PedidoView(View):
    def get(self, request):
        context_dict = {}
        context_dict['form'] = PedidoForm()
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        return render(request, 'pedidos/pedido.html', context_dict)

    def post(self, request):
        context_dict = {}
        form = PedidoForm(data=request.POST)
        pedido_ativo = SessaoPedido(request=request)
        if form.is_valid():
            pedido_novo = form.save()
            pedido_ativo.iniciar(pedido_novo.id)
            return HttpResponseRedirect(
                urlresolvers.reverse('visualizar_pedido', kwargs={'id_pedido': pedido_novo.id}) + '?criado=True')
        context_dict['mensagem'] = {'codigo': False, 'texto': 'Não foi possível registrar o pedido!'}
        context_dict['pedido_ativo'] = pedido_ativo.get_objeto_pedido()
        context_dict['form'] = form
        return render(request, 'pedidos/pedido.html', context_dict)

    @classmethod
    def Continuar(self, request, id_pedido):
        pedido = PedidoModel.get_or_none(id=id_pedido)
        if pedido:
            pedido_ativo = SessaoPedido(request=request)
            pedido_ativo.iniciar(pedido.id)
            pedido.finalizado = False
            pedido.save()
            return HttpResponseRedirect(
                urlresolvers.reverse('visualizar_pedido', kwargs={'id_pedido': pedido.id}) + '?reaberto=True')
        else:
            return HttpResponseNotFound('<h1>404</h1><p>Pedido %s não existe!' % id_pedido)

    @classmethod
    def Listar(self, request):
        context_dict = {}
        pedidos = PedidoModel.objects.all().order_by('-data')
        context_dict['pedidos'] = pedidos
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        context_dict['mensagem'] = self.get_pedido_mensagem(request=request)
        return render(request, 'pedidos/lista_pedidos.html', context_dict)

    @classmethod
    def Cancelar(self, request):
        pedido_ativo = SessaoPedido(request=request)
        pedido = pedido_ativo.get_objeto_pedido()
        if pedido:
            for item in ItemModel.objects.filter(pedido=pedido):
                item.delete()
        else:
            return HttpResponseNotFound('<h1>404</h1><p>Pedido %s inválido!')
        pedido_ativo.get_objeto_pedido().delete()
        pedido_ativo.excluir()
        return HttpResponseRedirect(urlresolvers.reverse('lista_pedidos') + '?cancelado=True')

    @classmethod
    def Finalizar(self, request):
        context_dict = {}
        pedido_atual = SessaoPedido(request=request)
        pedido = pedido_atual.get_objeto_pedido()
        if pedido:
            if pedido.itens.all().count() > 0:
                pedido.finalizado = True
                pedido.save()
                pedido_atual.excluir()
                return HttpResponseRedirect(
                    urlresolvers.reverse('visualizar_pedido', kwargs={'id_pedido': pedido.id}) + '?finalizado=True')
            else:
                mensagem = get_mensagem(view='pedido', mensagem='sem_itens')

            itens = ItemModel.objects.filter(pedido=pedido)
            context_dict['pedido'] = pedido
            context_dict['pedido_ativo'] = pedido
            context_dict['itens'] = itens
            context_dict['mensagem'] = mensagem
            return render(request, 'pedidos/visualizar_pedido.html', context_dict)
        else:
            return HttpResponseNotFound('<h1>404</h1><p>Pedido inexistente!')

    @classmethod
    def Visualizar(self, request, id_pedido):
        context_dict = {}
        pedido = PedidoModel.get_or_none(id=id_pedido)
        if pedido:
            itens = ItemModel.objects.filter(pedido=pedido)
            context_dict['pedido'] = pedido
            context_dict['itens'] = itens
            context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
            context_dict['valor_total'] = self.get_valor_total_pedido(itens)
            context_dict['mensagem'] = self.get_pedido_mensagem(request)
            return render(request, 'pedidos/visualizar_pedido.html', context_dict)
        else:
            return HttpResponseNotFound('<h1>404</h1><p>Pedido %s não existe!' % id_pedido)

    def get_valor_total_pedido(itens):
        total = 0
        for item in itens:
            total += item.preco * item.quantidade
        return total

    def get_pedido_mensagem(request):
        if request.GET.get('criado') == 'True':
            return {'codigo': True, 'texto': 'Pedido criado!'}
        elif request.GET.get('reaberto') == 'True':
            return {'codigo': True, 'texto': 'Pedido reaberto!'}
        elif request.GET.get('finalizado') == 'True':
            return {'codigo': True, 'texto': 'Pedido finalizado!'}
        elif request.GET.get('removido') == 'True':
            return {'codigo': True, 'texto': 'Item removido do pedido!'}
        elif request.GET.get('cancelado') == 'True':
            return {'codigo': True, 'texto': 'Pedido cancelado!'}
        else:
            return None
