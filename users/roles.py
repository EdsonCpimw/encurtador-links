from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        'Cadastrar_usuario': True,
        'listar_usuario': True,
        'Atualizar_usuario': True,
        'deletar_usuario': True,
        'detalhes_usuario': True,
        'Cadastrar_link': True,
        'listar_links': True,
        'deletar_link': True,
        'detalhes_link': True,
        'remover_links': True
    }



class Usuario(AbstractUserRole):
    available_permissions = {
        'Atualizar_usuario': True,
        'Cadastrar_link': True,
        'listar_links': True,
        'deletar_link': True,
        'detalhes_link': True
    }
