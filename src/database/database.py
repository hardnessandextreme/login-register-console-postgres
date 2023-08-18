import sys
from psycopg2 import pool
from src.registros.logs import log

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
    _MIN_CONN = 1
    _MAX_CONN = 5
    _pool = None

    @classmethod
    def obtenerPool(cls):
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(cls._MIN_CONN, cls._MAX_CONN,
                                                      database=cls._DATABASE,
                                                      user=cls._USER,
                                                      password=cls._PASSWORD,
                                                      host=cls._HOST,
                                                      port=cls._PORT)
                log.debug(f'Creacion del pool exitosa {cls._pool}')
                return cls._pool
            except Exception as e:
                log.error(f'Error en el pool: {e}')
                sys.exit()
        else:
            return cls._pool
    @classmethod
    def obtenerConexion(cls):
        conexion = cls.obtenerPool().getconn()
        log.debug(f'Conexion del pool ok: {conexion}')
        return conexion

    @classmethod
    def liberarConexion(cls, conexion):
        cls.obtenerPool().putconn(conexion)
        log.debug(f'Regresado la conexion al pool: {conexion}\n')

    @classmethod
    def cerrarConexiones(cls):
        cls.obtenerPool().closeall()
        log.debug(f'Se cerraron las conexiones')