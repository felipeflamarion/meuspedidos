# unicode: utf-8
from django.db import models

class ProdutoModel(models.Model):

    nome = models.CharField(max_length=50)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    multiplo = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'Produtos'