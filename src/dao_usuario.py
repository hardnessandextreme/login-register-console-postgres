from database import Database
from usuario import Usuario, UsuarioAdmin
from logs.logging import log


class DAOUsuario:
    # Variables que guardan las sentencias de los metodos.
    _REGISTRAR = 'INSERT INTO usuarios (name_user, pass_user) VALUES (%s, %s)'
    _VERIFICAR_USER_REGISTRO = 'SELECT * FROM usuarios WHERE name_user = %s'
    _LOGEAR = 'SELECT id_user FROM usuarios WHERE name_user = %s AND pass_user = %s'
    _VERIFICAR_ADMIN_USER = 'SELECT is_admin FROM usuarios WHERE name_user = %s'

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
                    print(cursor.fetchone())
                    print('El usuario ya existe, escoja otro.')
                    log.error(f'Error: El usuario {usuario.name_user} ya existe, escoja otro.')
                    registro_exitoso = False
                else:
                    valor_registro = (usuario.name_user, usuario.pass_user)
                    cursor.execute(cls._REGISTRAR, valor_registro)
                    print('Usuario registrado correctamente')
                    log.debug(f'Un usuario se registro correctamente: {usuario.name_user}')
                    registro_exitoso = True
            return registro_exitoso

    @classmethod
    def logearUsuario(cls, usuario):
        with Database.crearCursor() as cursor:
            inicio_exitoso = False
            valores_usuario = (usuario.name_user, usuario.pass_user)
            cursor.execute(cls._LOGEAR, valores_usuario)
            verificacion = cursor.fetchone()
            if verificacion:
                id_usuario = verificacion[0]
                inicio_exitoso = True
                print('Inicio de sesion exitoso.')
                log.debug(f'El usuario {usuario.name_user} con ID: {id_usuario} ha iniciado sesion.')
                return inicio_exitoso
        #     else:
        #         inicio_exitoso = False
        #         print('Credenciales invalidas.')
        #         log.error(f'Error: Credenciales invalidas. Usuario: {usuario.name_user} Contrasena: {usuario.pass_user}')
        # return inicio_exitoso

    @classmethod
    def esAdministrador(cls, usuario):
        # esAdmin = False
        with Database.conectarDb() as conexion:
            with conexion.cursor() as cursor:
                valores_usuario_admin = (usuario.name_user,)
                cursor.execute(cls._VERIFICAR_ADMIN_USER, valores_usuario_admin)
                valor_admin = cursor.fetchone()
                if valor_admin[0] == 'S':
                    esAdmin = True
                    # print('Es admin')
                else:
                    esAdmin = False
                    # print('No es admin')
            return esAdmin


# print('Registro de usuario')
# usuario = input('Ingrese el usuario: ')
# password = input('Ingrese la contrasenia: ')
# user1 = Usuario(name_user=usuario, pass_user=password)
# registro = DAOUsuario.registrarUsuario(user1)


# print('Inicio de sesion')
# usuario1 = input('Ingrese el usuario: ')
# password1 = input('Ingrese la contrasenia: ')
#
# user2 = Usuario(name_user=usuario1, pass_user=password1)
# inicio = DAOUsuario.logearUsuario(user2)

# print('Verificar usuario admin')
# usuario2 = input('Ingrese el usuario')
# user3 = Usuario(name_user=usuario2)
# adminVer = DAOUsuario.esAdministrador(user3)