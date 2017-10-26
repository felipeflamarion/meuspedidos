# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from pedidos.models import *

# Register your models here.
admin.site.register(ClienteModel)
admin.site.register(ProdutoModel)
admin.site.register(PedidoModel)
admin.site.register(ItemModel)
