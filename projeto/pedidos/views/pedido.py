# coding:utf-8
from django.core import urlresolvers
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from pedidos.forms import PedidoForm
from pedidos.models import PedidoModel
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

        if form.is_valid():
            pedido = form.save()
            pedido_ativo = SessaoPedido(request=request)
            if pedido_ativo.existe():
                pedido_ativo.excluir()
            pedido_ativo.inicializar(pedido.id)
            return HttpResponseRedirect(urlresolvers.reverse('lista_produtos'))
        else:
            mensagem = {'codigo': False, 'texto': 'Não foi possível registrar o pedido!'}

        context_dict['form'] = form
        context_dict['mensagem'] = mensagem
        return render(request, 'pedidos/pedido.html', context_dict)

    @classmethod
    def ListaPedidos(self, request):
        context_dict = {}
        pedidos = PedidoModel.objects.all()
        context_dict['pedidos'] = pedidos
        return render(request, 'pedidos/lista_pedidos.html', context_dict)

