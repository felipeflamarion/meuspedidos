"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from pedidos.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^inicio/$', IndexView.as_view(), name='index'),

    url(r'^pedido/$', PedidoView.as_view(), name='novo_pedido'),
    url(r'^pedidos/$', PedidoView.Listar, name='lista_pedidos'),
    url(r'^pedido/finalizar/$', PedidoView.Finalizar, name='finalizar_pedido'),
    url(r'^pedido/cancelar/$', PedidoView.Cancelar, name='cancelar_pedido'),
    url(r'^pedido/continuar/(?P<id_pedido>\d+)/$', PedidoView.Continuar, name='continuar_pedido'),
    url(r'^pedido/visualizar/(?P<id_pedido>\d+)/$', PedidoView.Visualizar, name='visualizar_pedido'),

    url(r'^produto/(?P<id_produto>\d+)/$', ProdutoView.Visualizar, name='visualizar_produto'),
    url(r'^produtos/$', ProdutoView.Listar, name='lista_produtos'),
    url(r'^produto/adicao-rapida/(?P<id_produto>\d+)$', ProdutoView.AdicaoRapida, name='adicao_rapida'),

    url(r'^item/$', ItemView.as_view(), name='novo_item'),
    url(r'^item/visualizar/(?P<id_item>\d+)/$', ItemView.Visualizar, name='visualizar_item'),
    url(r'^item/editar/(?P<id_item>\d+)/$', ItemView.Editar, name='editar_item'),
    url(r'^item/excluir/(?P<id_item>\d+)/$', ItemView.Excluir, name='excluir_item'),
]
