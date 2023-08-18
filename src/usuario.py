"""
Esta clase usuario contiene todas las columnas de la tabla en la cual vamos a trabajar. Estamos usando el patron
de disenio DAO. Que nos ayudara a enviar sentencias SQL desde la logica de negocio (interfaz de usuario). Cada
variable de instancia tiene su respectivo metodo setter y getter. Se le asigna por defecto None a todas las variables
de clase para no tener que especificar cada una al momento de usarlas.
"""


class Usuario:
    def __init__(self, id_user=None, name_user=None, pass_user=None, is_admin=False):
        self._id_user = id_user
        self._name_user = name_user
        self._pass_user = pass_user
        self._is_admin = is_admin

    def __str__(self):
        return f'id: {self._id_user} nombre: {self._name_user} admin: {self._is_admin}'

    @property
    def name_user(self):
        return self._name_user

    @name_user.setter
    def name_user(self, name_user):
        self._name_user = name_user

    @property
    def pass_user(self):
        return self._pass_user

    @pass_user.setter
    def pass_user(self, pass_user):
        self._pass_user = pass_user

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, is_admin):
        self._is_admin = is_admin

    @property
    def id_user(self):
        return self._id_user

    @id_user.setter
    def id_user(self, id_user):
        self._id_user = id_user