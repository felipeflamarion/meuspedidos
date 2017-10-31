# coding:utf-8
from django.core import urlresolvers
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from pedidos.forms import PedidoForm
from pedidos.models import PedidoModel, ItemModel
from pedidos.views.functions import SessaoPedido

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
            if pedido_ativo.existe():
                pedido_ativo.excluir()
            pedido_ativo.iniciar(pedido_novo.id)
            return HttpResponseRedirect(urlresolvers.reverse('visualizar_pedido', kwargs={'id_pedido': pedido_novo.id}) + '?criado=True')

        context_dict['mensagem'] = {'codigo': False, 'texto': 'Não foi possível registrar o pedido!'}
        context_dict['pedido_ativo'] = pedido_ativo.get_objeto_pedido()
        context_dict['form'] = form
        return render(request, 'pedidos/pedido.html', context_dict)

    @classmethod
    def Continuar(self, request, id_pedido):
        try:
            pedido = PedidoModel.objects.get(pk=id_pedido)
        except PedidoModel.DoesNotExist:
            return HttpResponseNotFound('<h1>404</h1><p>Pedido %s não existe!' %id_pedido)
        pedido_ativo = SessaoPedido(request=request)
        if pedido_ativo.existe():
            pedido_ativo.excluir()
        pedido_ativo.iniciar(pedido.id)
        pedido.finalizado = False
        pedido.save()
        return HttpResponseRedirect(urlresolvers.reverse('visualizar_pedido', kwargs={'id_pedido': pedido.id}) + '?reaberto=True')

    @classmethod
    def Listar(self, request):
        context_dict = {}
        pedidos = PedidoModel.objects.all().order_by('-data')
        context_dict['pedidos'] = pedidos
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        if request.GET.get('cancelado') == 'True':
            context_dict['mensagem'] = {'codigo': True, 'texto': 'Pedido cancelado!'}
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
            if len(pedido.itens.all()) > 0:
                pedido.finalizado = True
                pedido.save()
                pedido_atual.excluir()
                return HttpResponseRedirect(urlresolvers.reverse('visualizar_pedido', kwargs={'id_pedido': pedido.id}) + '?finalizado=True')
            else:
                mensagem = {'codigo': False, 'texto': 'Um pedido deve conter pelo menos 1 item!'}
        else:
            return HttpResponseNotFound('<h1>404</h1><p>Pedido %s inválido!')

        itens = ItemModel.objects.filter(pedido=pedido)
        context_dict['pedido'] = pedido
        context_dict['pedido_ativo'] = pedido
        context_dict['itens'] = itens
        context_dict['mensagem'] = mensagem
        return render(request, 'pedidos/visualizar_pedido.html', context_dict)

    @classmethod
    def Visualizar(self, request, id_pedido):
        context_dict = {}
        try:
            pedido = PedidoModel.objects.get(pk=id_pedido)
        except PedidoModel.DoesNotExist:
            return HttpResponseNotFound('<h1>404</h1><p>Pedido %s não existe!' %id_pedido)
        itens = ItemModel.objects.filter(pedido=pedido)
        context_dict['pedido'] = pedido
        context_dict['itens'] = itens
        context_dict['valor_total'] = self.valor_total(itens)
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()

        if request.GET.get('criado') == 'True':
            context_dict['mensagem'] = {'codigo': True, 'texto': 'Pedido criado!'}
        elif request.GET.get('reaberto') == 'True':
            context_dict['mensagem'] = {'codigo': True, 'texto': 'Pedido reaberto!'}
        elif request.GET.get('finalizado') == 'True':
            context_dict['mensagem'] = {'codigo': True, 'texto': 'Pedido finalizado!'}
        elif request.GET.get('removido') == 'True':
            context_dict['mensagem'] = {'codigo': True, 'texto': 'Item removido do pedido!'}
        return render(request, 'pedidos/visualizar_pedido.html', context_dict)

    def valor_total(itens):
        total = 0
        for item in itens:
            total += item.preco * item.quantidade
        return total

