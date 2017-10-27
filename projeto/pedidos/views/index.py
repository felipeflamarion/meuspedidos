# coding:utf-8
from django.shortcuts import render
from django.views import View
from pedidos.views.functions import SessaoPedido

class IndexView(View):

    def get(self, request):
        context_dict = {}
        context_dict['pedido_ativo'] = SessaoPedido(request=request).get_objeto_pedido()
        return render(request, 'pedidos/index.html', context_dict)