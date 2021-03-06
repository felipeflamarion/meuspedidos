# coding: utf-8
from django.db import models
from pedidos.models import ClienteModel, ProdutoModel


class PedidoModel(models.Model):
    itens = models.ManyToManyField(ProdutoModel, through='ItemModel')
    cliente = models.ForeignKey(ClienteModel)
    data = models.DateTimeField(auto_now_add=True)
    finalizado = models.BooleanField(default=False)

    def get_or_none(id):
        try:
            return PedidoModel.objects.get(pk=id)
        except:
            return None

    def __str__(self):
        return '%s %s em %s' % (self.cliente.nome, self.cliente.sobrenome, self.data.strftime(u'%d/%m/%Y em %H:%M'))

    class Meta:
        verbose_name_plural = 'Pedidos'
