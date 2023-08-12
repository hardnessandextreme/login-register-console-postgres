from database import Database
from usuario import Usuario
from logs.logging import log

"""
La clase DAOUsuario contiene todos los metodos que el usuario va a tener para realizar las operaciones.
Las sentencias SQL se guardan en una variable descriptiva, esto se hace con el fin de ahorrar espacio y
tener mejor legibilidad.
"""


class DAOUsuario:
    # Variables que guardan las sentencias de los metodos.
    _REGISTRAR = 'INSERT INTO usuarios (name_user, pass_user) VALUES (%s, %s)'
    _VERIFICAR_USER_REGISTRO = 'SELECT * FROM usuarios WHERE name_user = %s'
    _LOGEAR = 'SELECT id_user FROM usuarios WHERE name_user = %s AND pass_user = %s'
    _VERIFICAR_ADMIN_USER = 'SELECT is_admin FROM usuarios WHERE name_user = %s'
    _EXTRAER_ID_USUARIO_A_SUBIR = 'SELECT id_user FROM usuarios WHERE name_user = %s'
    _CONVERTIR_ADMIN = "UPDATE usuarios SET is_admin='S' WHERE name_user= %s"
    _LISTAR_USUARIOS = 'SELECT * FROM usuarios ORDER BY id_user'
    _CAMBIAR_CONTRASENA = 'UPDATE usuarios SET pass_user = %s WHERE name_user = %s'
    _CONF_CONTRA_ACTUAL = 'SELECT pass_user FROM usuarios WHERE name_user=%s'

    """
    El metodo de clase registrarUsuario tomo como parametro (o tiene como argumento) un objeto instanciado de la 
    clase Usuario. Se usa el with para tener un control en el cierre de conexiones y de cursores. Primero se hace una 
    validacion del usuario, si existe o no existe. Se extrae el atributo .name_user, del objeto pasado como 
    parametro y lo verifica con la sentencia _VERIFICAR_USER_REGISTRO. Si el fetchone retorna un valor que no sea None,
    le avisa al usuario que su nombre de usuario ya existe. Caso contrario se ejecuta la sentencia _REGISTRAR con los 
    datos proporcionados.
    """

    @classmethod
    def registrarUsuario(cls, usuario):
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

    """
    Este otro metodo de clase logearUsuario() ayudara a al usuario a poder iniciar sesion.
    De igual forma se manejan con with para controlar los cierres de conexion y de cursores automaticamente.
    Se hace uso de la sentencia _LOGEAR junto al atributo extraido del objeto instanciado pasado como parametro.
    Este metodo tambien extrae el ID del usuario para poder mostrarlo en los logs.
    Devuelve un booleano, si el registro es exitoso retorna True caso contrario False.
    """

    @classmethod
    def logearUsuario(cls, usuario):
        with Database.conectarDb() as conexion:
            with conexion.cursor() as cursor:
                valores_usuario = (usuario.name_user, usuario.pass_user)
                cursor.execute(cls._LOGEAR, valores_usuario)
                verificacion = cursor.fetchone()
                if verificacion:
                    usuario.id_user = verificacion[0]
                    inicio_exitoso = True
                    print('\nInicio de sesion exitoso.\n')
                    log.debug(f'El usuario {usuario.name_user} con ID: {usuario.id_user} ha iniciado sesion.')
                else:
                    inicio_exitoso = False
            return inicio_exitoso

    """
    El metodo de clase esAdministrador() asiste al sistema para verificar si un usuario que inicia sesion, tiene
    privilegios de administrador. Se ejecuta la setencia _VERIFICAR_ADMIN_USER junto al atributo del usuario pasado por
    parametro. Luego se extrae ese valor de la consulta y se realizar una validacion. La consulta arroja 'S' es porque
    es el usuario es administrador y se le asigna a la variable esAdmin = True caso contrario se le asigna False.
    Retorna la variable esAdmin dependiendo del resultado.
    """

    @classmethod
    def esAdministrador(cls, usuario):
        with Database.conectarDb() as conexion:
            with conexion.cursor() as cursor:
                valores_usuario_admin = (usuario.name_user,)
                cursor.execute(cls._VERIFICAR_ADMIN_USER, valores_usuario_admin)
                valor_admin = cursor.fetchone()
                if valor_admin[0] == 'S':
                    esAdmin = True
                else:
                    esAdmin = False
            return esAdmin

    """
    convetirAdmin() es un metodo que contiene dos cursores y sirve para poder dar rango administrador a un usuario 
    por su nombre. El primer cursor usa la sentencia _EXTRAER_ID_USUARIO_A_SUBIR para obtener el id del usuario a ser 
    elevado. El segundo cursor sirve ejecuta la sentencia _CONVERTIR_ADMIN para cambiar el estado. de la columna 
    is_admin ('N') de la tabla por 'S'
    """

    @classmethod
    def convertirAdmin(cls, usuario):
        with Database.conectarDb() as conexion:
            with conexion.cursor() as cursor1:
                valor = (usuario.name_user,)
                cursor1.execute(cls._EXTRAER_ID_USUARIO_A_SUBIR, valor)
                valor_admin = cursor1.fetchone()
                usuario.id_user = valor_admin[0]

            with conexion.cursor() as cursor:
                valores = (usuario.name_user,)
                cursor.execute(cls._CONVERTIR_ADMIN, valores)

    """
    Este metodo es sencillo, sirve para listar los usuarios y solo se llama cuando un administrador accede a esa 
    opcion. El fetchall retornado se recorre con un for para ir guardando las tuplas en una lista. Retorna la lista 
    de tuplas con los resultados de la sentencia _LISTAR_USUARIOS.
    """

    @classmethod
    def listarUsuarios(cls):
        with Database.conectarDb() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(cls._LISTAR_USUARIOS)
                registros = cursor.fetchall()
                listaUsuarios = []
                for usuario in registros:
                    usuarios = Usuario(id_user=usuario[0], name_user=usuario[1], pass_user=usuario[2],
                                       is_admin=usuario[3])
                    listaUsuarios.append(usuarios)
                return listaUsuarios

    @classmethod
    def cambiarContrasenia(cls, usuario, contrasenia_actual, contrasnia_a_cambiar):
        with Database.conectarDb() as conexion:
            with conexion.cursor() as cursor:
                valores = (usuario.name_user,)
                cursor.execute(cls._CONF_CONTRA_ACTUAL, valores)
                verificacion = cursor.fetchone()
                if verificacion[0] != contrasenia_actual:
                    print('La contrasena actual no coincide')
                    cambio = False
                else:
                    valores = (contrasnia_a_cambiar, usuario.name_user)
                    cursor.execute(cls._CAMBIAR_CONTRASENA, valores)
                    print('Has actualizado tu contrasenia.')
                    cambio = True
            return cambio