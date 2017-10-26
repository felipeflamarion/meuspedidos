# unicode: utf-8
from django.db import models
from pedidos.models import ClienteModel, ProdutoModel

class PedidoModel(models.Model):

    itens = models.ManyToManyField(ProdutoModel, through='ItemModel')
    cliente = models.ForeignKey(ClienteModel)
    data = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Pedidos'
