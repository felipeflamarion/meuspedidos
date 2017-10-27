# coding:utf-8
from django import forms

from pedidos.models import ItemModel

class ItemForm(forms.ModelForm):

    class Meta:
        model = ItemModel
        fields = ('quantidade', 'preco')