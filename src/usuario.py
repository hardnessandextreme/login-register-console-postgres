class Usuario:
    def __init__(self, id_user=None, name_user=None, pass_user=None, is_admin=False):
        self._id_user = id_user
        self._name_user = name_user
        self._pass_user = pass_user
        self._is_admin = is_admin
    
    def __str__(self):
        return (f'id: {self._id_user}\n'
                f'nombre: {self._name_user}\n'
                f'admin: {self._is_admin}')
    
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
    

class UsuarioAdmin(Usuario):
    def __init__(self, id_user=None, name_user=None, pass_user=None, is_admin=True):
        super().__init__(id_user, name_user, pass_user, is_admin)