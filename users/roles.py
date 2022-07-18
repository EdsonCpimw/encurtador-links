from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        'Cadastrar_usuario': True,
        'listar_usuario': True,
        'Atualizar_usuario': True,
        'deletar_usuario': True,
        'detalhes_usuario': True

    }



class Usuario(AbstractUserRole):
    available_permissions = {

    }