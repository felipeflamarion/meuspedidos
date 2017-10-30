# MeusPedidos
*Disponível em* http://flamarion.pythonanywhere.com/inicio/

__Autor:__ Felipe Flamarion da Conceição

__Data:__ 2017-10-26

__Linguagem:__ Python 3.5 (Django Framework 1.11)

__Banco de Dados:__ SQLite

## Instalação

1. git clone https://github.com/felipeflamarion/meuspedidos.git
2. virtualenv -p python3 nome_virtualenv
3. cd meuspedidos/projeto/
4. pip install -r requirements.txt
5. python manage.py makemigrations
6. python manage.py migrate
7. python populate.py
8. python manage.py runserver

### RF - Requisitos Funcionais
* O sistema deve permitir (CRUD) o cadastro de pedidos;
* O sistema deve listar os produtos ofertados;
* O sistema deve sugerir o preço unitário do produto;

### RNF - Requisitos Não Funcionais
* O sistema deve ser hospedado em um serviço de hospedagem gratuito;

### RN - Regras de Negócio
* A quantidade de produto deve ser um número inteiro maior que zero;
* O preço de produto deve ter no máximo duas casas decimais e precisa ser maior que zero;
* O sistema deve possuir três níveis de rentabilidade: ótima, boa e ruim;
* Alguns produtos podem ser vendidos somente em quantidade múltiplas predeterminadas.

#### Tabelas

##### Cliente
* id __(PK)__
* nome

##### Produto
* id __(PK)__
* nome
* preco_unitario
* multiplo

##### Pedido
* id __(PK)__
* cliente __(FK)__
* data
* finalizado

##### Item
* produto __(PK)__ __(FK)__
* pedido __(PK)__ __(FK)__
* preco
* quantidade

#### Rentabilidades:
* Rentabilidade ótima: quando o preço usado no pedido é maior que o preço do produto;
* Rentabilidade boa: quando o preço do item é no máximo 10% menor que o preço do produto;
* Rentabilidade ruim: preço do item é inferior ao preço do produto menos 10%;
