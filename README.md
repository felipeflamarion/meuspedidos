# MeusPedidos
*Dispon?vel em (em breve no PythonAnyWhere)*

__Autor:__ Felipe Flamarion da Concei??o

__Data:__ 2017-10-26

__Linguagem:__ Python (Django Framework)

__Banco de Dados:__ SQLite

### RF - Requisitos Funcionais
* O sistema deve permitir (CRUD) o cadastro de pedidos;
* O sistema deve listar os produtos ofertados;
* O sistema deve sugerir o pre?o unit?rio do produto;

### RNF - Requisitos N?o Funcionais
* O sistema deve ser hospedado em qualquer servi?o de hospedagem gratuito;

### RN - Regras de Neg?cio
* A quantidade de produto deve ser um n?mero inteiro maior que zero;
* O pre?o de produto deve ter no m?ximo duas casas decimais e precisa ser maior que zero;
* O sistema deve possuir tr?s n?veis de rentabilidade: ?tima, boa e ruim (Descri??o das rentabilidades no fim do documento);
* Alguns produtos podem ser vendidos somente em quantidade m?ltiplas.

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
* ativo

##### Item
* produto __(PK)__ __(FK)__
* pedido __(PK)__ __(FK)__
* preco

Composi??o do elemento Pedido:
* Cliente;
* Itens: produto, quantidade, pre?o unit?rio;

#### Rentabilidade:
* Rentabilidade ?tima: quando o pre?o usado no pedido ? maior que o pre?o do produto;
* Rentabilidade boa: quando o pre?o do item ? no m?ximo 10% menor que o pre?o do produto;
* Rentabilidade ruim: pre?o do item ? inferior ao pre?o do produto menos 10%;
