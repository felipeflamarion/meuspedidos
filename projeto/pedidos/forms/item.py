# coding:utf-8
from django import forms

from pedidos.models import ItemModel


class ItemForm(forms.ModelForm):
    quantidade = forms.IntegerField(min_value=1)

    def clean_preco(self):
        preco = self.cleaned_data['preco']
        if float(preco) > 0:
            return preco
        raise forms.ValidationError("O preço mínimo é R$ 0,01!")

    def __init__(self, quantidade=None, preco=None, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        if quantidade:
            self.fields['quantidade'].initial = quantidade
        if preco:
            self.fields['preco'].initial = preco

    class Meta:
        model = ItemModel
        fields = ('quantidade', 'preco')
