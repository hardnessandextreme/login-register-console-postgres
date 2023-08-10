import psycopg2 as db
import sys
from logs.logging import log

class Database:
    _DATABASE='sistema_prueba'
    _USER='postgres'
    _PASSWORD='admin'
    _HOST='127.0.0.1'
    _PORT='5432'
    _conexion=None
    _cursor=None


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
                log.debug('Se conecto la base de datos satisfactoriamente.')
                return cls._conexion
            except Exception as e:
                log.error('No se logro conectar a la base de datos.')
                sys.exit()
        else:
            return cls._conexion


    @classmethod
    def crearCursor(cls):
        if cls._cursor is None:
            try:
                cls._cursor = cls.conectarDb().cursor()
                log.debug('Se creo el cursor correctamente.')
                return cls._cursor
            except Exception as e:
                log.error('No se logro crear el cursor.')
        else:
            return cls._cursor