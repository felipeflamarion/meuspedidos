# coding:utf-8
from django.core import urlresolvers
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
    def Listar(self, request):
        context_dict = {}
        pedidos = PedidoModel.objects.all()
        context_dict['pedidos'] = pedidos
        return render(request, 'pedidos/lista_pedidos.html', context_dict)

    @classmethod
    def Cancelar(self, request):
        context_dict = {}
        sessao_pedido = SessaoPedido(request=request)
        pedido = sessao_pedido.get_objeto_pedido()
        for item in ItemModel.objects.filter(pedido=pedido):
             item.delete()
        sessao_pedido.excluir()
        pedido.delete()
        return render(request, 'pedidos/lista_pedidos.html', context_dict)

    @classmethod
    def Finalizar(self, request):
        context_dict = {}
        sessao_pedido = SessaoPedido(request=request)
        pedido = sessao_pedido.get_objeto_pedido()
        if pedido:
            if len(pedido.itens.all()) > 0:
                pedido.finalizado = True
                pedido.save()
                sessao_pedido.excluir()
                mensagem = {'codigo': True, 'texto': 'Pedido finalizado com sucesso!'}
            else:
                mensagem = {'codigo': False, 'texto': 'Um pedido deve conter pelo menos 1 item!'}
        else:
            mensagem = {'codigo': False, 'texto': 'Não foi possível finalizar. Pedido inválido!'}

        itens = ItemModel.objects.filter(pedido=pedido)
        context_dict['pedido'] = pedido
        context_dict['itens'] = itens
        context_dict['sessao_pedido'] = sessao_pedido.get_objeto_pedido()
        return render(request, 'pedidos/visualizar_pedido.html', context_dict)

    @classmethod
    def Visualizar(self, request, id_pedido):
        context_dict = {}
        sessao_pedido = SessaoPedido(request=request)
        pedido = PedidoModel.objects.get(pk=id_pedido)
        itens = ItemModel.objects.filter(pedido=pedido)
        context_dict['pedido'] = pedido
        context_dict['itens'] = itens
        context_dict['sessao_pedido'] = sessao_pedido.get_objeto_pedido()
        return render(request, 'pedidos/visualizar_pedido.html', context_dict)

