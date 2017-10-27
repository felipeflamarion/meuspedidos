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
    url(r'^pedidos/$', PedidoView.ListaPedidos, name='lista_pedidos'),
    url(r'^pedido/cancelar/$', PedidoView.CancelarPedido, name='cancelar_pedido'),

    url(r'^produto/(?P<id_produto>\d+)/$', ProdutoView.Visualizar, name='visualizar_produto'),
    url(r'^produtos/$', ProdutoView.ListaProdutos, name='lista_produtos'),

    url(r'^item/$', ItemView.as_view(), name='novo_item'),
]
