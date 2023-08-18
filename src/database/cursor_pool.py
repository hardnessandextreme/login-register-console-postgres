import time
from src.database.database import Database
from src.registros.logs import log

class CursorPool:
    def __init__(self):
        self._conexion = None
        self._cursor = None

    def __enter__(self):
        log.debug('Entrando al cursor con __enter__')
        self._conexion = Database.obtenerConexion()
        self._cursor = self._conexion.cursor()
        return self._cursor

    def __exit__(self, exc_tipo, exc_valor, exc_detalle):
        log.debug('Cerrancdo el cursor con __exit__')
        if exc_tipo:
            self._conexion.rollback()
            log.error(f'Ocurrio un error, se hace rollback: \n'
                      f'Valor del error: {exc_valor}\n'
                      f'Tipo del error: {exc_tipo}\n'
                      f'Detalle del error: {exc_detalle}\n')
        else:
            self._conexion.commit()
            log.debug('Se realizo el commit correctamente')
        self._cursor.close()
        Database.liberarConexion(self._conexion)