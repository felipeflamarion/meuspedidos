# unicode: utf-8
from django.db import models
from pedidos.models import ProdutoModel, PedidoModel

class ItemModel(models.Model):

    produto = models.ForeignKey(ProdutoModel)
    pedido = models.ForeignKey(PedidoModel)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Itens'