import psycopg2 as db
import sys
from logs.logging import log

"""
Se crea la clase Database que contendra toda la informacion de la base de datos.
Esta informacion contiene: la url de conoexion(namedb, user, password, host, port),
y tambien variables que guarden la conexion y el cursor.
"""


class Database:
    _DATABASE = 'sistema_prueba'
    _USER = 'postgres'
    _PASSWORD = 'admin'
    _HOST = '127.0.0.1'
    _PORT = '5432'
    _conexion = None
    _cursor = None

    """
    Este metodo de clase 'conectarDb()', verifica que si no existe una conexion va a intentar abrir una.
    En caso de que exista una conexion abierta, la va a retornar de todas formas.
    Se hace uso del modulo psycopg2 (renombrado como 'db'). Llamamos al metodo connect y pasamos como,
    parametro las variables que guardan el url de la base de datos.

    Una vez creada, retorna la conexion y se crea un log a nivel debug, si ocurre un error en la conexion,
    se envia un log a nivel error y se cierra el programa. El metodo esta creado con el fin de abrir conexiones directas
    a la base de datos para realizar operaciones.
    """

    @classmethod
    def conectarDb(cls):
        if cls._conexion is None:
            try:
                cls._conexion = db.connect(
                    database=cls._DATABASE,
                    user=cls._USER,
                    password=cls._PASSWORD,
                    host=cls._HOST,
                    port=cls._PORT
                )
                log.debug(f'Se conecto la base de datos satisfactoriamente. {cls._conexion}')
                return cls._conexion
            except Exception as e:
                log.error(f'No se logro conectar a la base de datos. {e}')
                sys.exit()
        else:
            return cls._conexion

    """
    El metodo de clase crearCursor() comprueba si no existe algun cursor abierto, si es asi intenta asignarle,
    a la variable de clase _cursor una conexion indirecta.
    """

    @classmethod
    def crearCursor(cls):
        if cls._cursor is None:
            try:
                cls._cursor = cls.conectarDb().cursor()
                log.debug(f'Se creo el cursor correctamente. {cls._cursor}')
                return cls._cursor
            except Exception as e:
                log.error(f'No se logro crear el cursor. {e}')
        else:
            return cls._cursor
