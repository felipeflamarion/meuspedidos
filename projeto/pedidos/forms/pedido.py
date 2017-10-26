# coding:utf-8
from django import forms
from pedidos.models import PedidoModel

class PedidoForm(forms.ModelForm):

    class Meta:
        model = PedidoModel
        fields = ('cliente', 'ativo')