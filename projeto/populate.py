# coding:utf-8
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from pedidos.models import ClienteModel, ProdutoModel


def populate():
    add_cliente(id=1, nome="Darth", sobrenome="Vader")
    add_cliente(id=2, nome="Obi-Wan", sobrenome="Kenobi")
    add_cliente(id=3, nome="Luke", sobrenome="Skywalker")
    add_cliente(id=4, nome="Imperador", sobrenome="Palpatine")
    add_cliente(id=5, nome="Han", sobrenome="Solo")

    add_produto(id=1, nome="Millenium Falcon", preco_unitario=550000.00, multiplo=1)
    add_produto(id=2, nome="X-Wing", preco_unitario=60000.00, multiplo=2)
    add_produto(id=3, nome="Super Star Destroyer", preco_unitario=4570000.00, multiplo=1)
    add_produto(id=4, nome="TIE Fighter", preco_unitario=75000.00, multiplo=2)
    add_produto(id=5, nome="Lightsaber", preco_unitario=6000.00, multiplo=5)
    add_produto(id=6, nome="DLT-19 Heavy Blaster Rifle", preco_unitario=5800.00, multiplo=1)
    add_produto(id=7, nome="DL-44 Heavy Blaster Pistol", preco_unitario=1500.00, multiplo=10)


def add_cliente(id, nome, sobrenome):
    cliente = ClienteModel.objects.get_or_create(id=id, nome=nome, sobrenome=sobrenome)[0]
    cliente.save()
    return cliente

def add_produto(id, nome, preco_unitario):
    produto = ProdutoModel.objects.get_or_create(id=id, nome=nome, preco_unitario=preco_unitario, multiplo=multiplo)[0]
    produto.save()
    return produto

if __name__ == '__main__':
    print("Populando o Banco de Dados do Projeto...")
    populate()
    print("Concluído!")