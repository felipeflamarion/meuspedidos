# coding:utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from pedidos.forms import PedidoForm
from pedidos.models import PedidoModel


class PedidoView(View):

    def get(self, request):
        context_dict = {}
        context_dict['form'] = PedidoForm()
        return render(request, 'pedidos/pedido.html', context_dict)

    def post(self, request):
        context_dict = {}
        form = PedidoForm(data=request.POST)

        if form.is_valid():
            form.save()
            mensagem = {'codigo': True, 'texto': 'Pedido registrado com sucesso!'}
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