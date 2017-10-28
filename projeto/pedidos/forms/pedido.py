# coding:utf-8
from django import forms
from pedidos.models import PedidoModel, ClienteModel


class PedidoForm(forms.ModelForm):

    cliente = forms.ModelChoiceField(
        required=True,
        queryset=ClienteModel.objects.all(),
        widget=forms.Select(attrs={"class": "ui fluid search selection dropdown"})
    )

    class Meta:
        model = PedidoModel
        fields = ('cliente',)