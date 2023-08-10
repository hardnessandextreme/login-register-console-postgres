from database import Database
from usuario import Usuario, UsuarioAdmin
from logs.logging import log


class DAOUsuario:
    # Variables que guardan las sentencias de los metodos.
    _REGISTRAR = 'INSERT INTO usuarios (name_user, pass_user) VALUES (%s, %s)'
    _VERIFICAR_USER_REGISTRO = 'SELECT * FROM usuarios WHERE name_user = %s'
    _LOGEAR = 'SELECT id_user FROM usuarios WHERE name_user = %s AND pass_user = %s'
    _VERIFICAR_USER = 'SELECT is_admin FROM usuarios WHERE name_user = %s'

    # Sentencias de escritura deben abrir la conexion y luego usar el cursor, no usar el cursor del metodo de clase
    # de clase database.py
    @classmethod
    def registrarUsuario(cls, usuario):
        registro_exitoso = None
        with Database.conectarDb() as conexion:
            with conexion.cursor() as cursor:
                valor_usuario = (usuario.name_user,)
                cursor.execute(cls._VERIFICAR_USER_REGISTRO, valor_usuario)
                if cursor.fetchone() is not None:
                    print('El usuario ya existe, escoja otro.')
                    log.error('El usuario ya existe, escoja otro.')
                    registro_exitoso = False
                else:
                    valor_registro = (usuario.name_user, usuario.pass_user)
                    cursor.execute(cls._REGISTRAR, valor_registro)
                    print('Usuario registrado correctamente')
                    log.debug('Usuario registrado correctamente')
                    registro_exitoso = True
            return registro_exitoso



print('Registro de usuario')
usuario = input('Ingrese el usuario: ')
password = input('Ingrese la contrasenia: ')
user1 = Usuario(name_user=usuario, pass_user=password)
registro = DAOUsuario.registrarUsuario(user1)
