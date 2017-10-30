# coding:utf-8
from pedidos.models import PedidoModel


class SessaoPedido:
    def __init__(self, request):
        self.request = request

    def iniciar(self, id_pedido):
        self.request.session['pedido'] = id_pedido

    def excluir(self):
        if self.existe():
            del self.request.session['pedido']

    def existe(self):
        if 'pedido' in self.request.session:
            return True
        return False

    def get(self):
        if self.existe():
            return int(self.request.session['pedido'])
        return None

    def get_objeto_pedido(self):
        id_pedido = self.get()
        try:
            return PedidoModel.objects.get(pk=id_pedido)
        except:
            return None
