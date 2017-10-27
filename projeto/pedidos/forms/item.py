# coding:utf-8
from django import forms

from pedidos.models import ItemModel

class ItemForm(forms.ModelForm):

    preco = forms.DecimalField()

    def __init__(self, quantidade=None, preco=None, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        if quantidade:
            self.fields['quantidade'].initial = quantidade
        if preco:
            self.fields['preco'].initial = preco

    class Meta:
        model = ItemModel
        fields = ('quantidade', 'preco')