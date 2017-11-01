# coding:utf-8

def get_mensagem(view, mensagem):
    mensagens = {
        'item': {
            'item_editado': {'codigo': True, 'texto': 'Item editado!'},
            'quantidade_invalida': {'codigo': False, 'texto': 'Quantidade inválida (deve-se respeitar o valor múltiplo de venda do produto)'},
            'cadastro_falhou': {'codigo': False, 'texto': 'Não foi possível adicionar o item!'},
            'edicao_falhou': {'codigo': False, 'texto': 'Não foi possível editar o item!'},
            'pedido_nao_finalizado': {'codigo': False, 'texto': 'Não é permitido modificar itens de pedidos finalizados!'}
        },
        'pedido': {
            'sem_itens': {'codigo': False, 'texto': 'Um pedido deve conter pelo menos 1 item!'}
        },
        'produto': {

        }
    }
    return mensagens[view][mensagem]