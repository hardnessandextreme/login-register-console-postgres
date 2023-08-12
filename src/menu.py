from dao_usuario import DAOUsuario, Usuario
from logs.logging import log


def iniciarSesion():
    print(' Inicio de Sesion '.center(50, '-'))
    name_user = input('Ingrese su usuario: ')
    contra = input('Ingrese su contrasenia: ')

    if (name_user == '') or (contra == ''):
        print('Rellene todos los campos')
        return

    usuario = Usuario(name_user=name_user, pass_user=contra)
    usuarioDAO = DAOUsuario.logearUsuario(usuario)

    if usuarioDAO:
        print('-' * 50)
        print('{:^50}'.format(f' Bienvenido al sistema {usuario.name_user} '))
        print('-' * 50)
        usuarioAdmin = DAOUsuario.esAdministrador(usuario)

        if not usuarioAdmin:
            menu = ('1. Cambiar tu contrasena\n'
                    '2. Ver tu nombre\n'
                    '3. Salir')
        else:
            menu = ('1. Crear usuario administrador\n'
                    '2. Cambiar tu contrasena\n'
                    '3. Ver tu nombre\n'
                    '4. Salir')
        while True:
            print(menu)
            opcion = int(input('Elige una opcion: '))

            if opcion == 1 and usuarioAdmin:
                print('Vas a crear un usuario admin')
                listado = DAOUsuario.listarUsuarios()
                for usersLista in listado:
                    print(usersLista)

                name_user = input('Ingrese el nombre del usuario a convertir a admin: ')
                user = Usuario(name_user=name_user)
                DAOUsuario.convertirAdmin(user)
                log.debug(f'(ID: {usuario.id_user}) {usuario.name_user} ha dado rango admin a (ID: {user.id_user})'
                          f' {user.name_user}')

            elif opcion == 2 and usuarioAdmin:
                print('Vas a cambiar tu contra')

            elif opcion == 3 and usuarioAdmin:
                print(f'Estas viendo tu nombre: {usuario.name_user}')

            elif opcion == 4 and usuarioAdmin:
                print('Estas saliendo')
                break

            elif opcion == 1:
                print('Vas a cambiar tu contra')

            elif opcion == 2:
                print(f'Estas viendo tu nombre: {usuario.name_user}')

            elif opcion == 3:
                print('Estas saliendo')
                break

            else:
                print('Opcion invalida, intenta de nuevo.')


def registrarUsuario():
    print(' Registro de usuario '.center(50, '-'))
    print('Consejos:\n'
          '1. El usuario debe tener al menos 3 caracteres y maximo 20.\n'
          '2. La contrasena debe tener al menos 8 caracteres, entre ellos: 1 numero, 1 letra mayuscula.\n'
          '3. La contrasena no debe exceder los 20 caracteres.'
          '4. La confirmacion de la contrasena debe ser igual a la contrasena.\n')
    name_user = input('Ingrese su usuario: ')
    pass_user = input('Ingrese su contrasena: ')
    conf_pass_user = input('Confirme su contrasena: ')

    # Validaciones:
    longitud_usuario = len(name_user) < 3
    longitud_usuario_maximo = len(name_user) > 20
    usuario_igual_pass = pass_user == name_user
    pass_no_tiene_numero = not any(c.isdigit() for c in pass_user)
    pass_no_tiene_mayus = not any(c.isupper() for c in pass_user)
    pass_no_conf_pass = pass_user != conf_pass_user
    pass_excede_limite = len(pass_user) > 20
    pass_no_supera_minimo = not len(pass_user) >= 8

    validacion_pass = (longitud_usuario or usuario_igual_pass or pass_no_tiene_numero or pass_no_tiene_mayus or
                       pass_no_conf_pass or pass_excede_limite or
                       pass_no_supera_minimo or longitud_usuario_maximo)

    if validacion_pass:
        print('Error: lea las indicaciones.')
    else:
        usuario = Usuario(name_user=name_user, pass_user=pass_user)
        DAOUsuario.registrarUsuario(usuario)


loop = True

while loop:
    print('Menu')
    print('1. Iniciar Sesion\n'
          '2. Registrarse\n'
          '3. Salir')

    try:
        choice = int(input('Ingrese una opcion: '))

        if choice == 1:
            iniciarSesion()
        elif choice == 2:
            registrarUsuario()
        elif choice == 3:
            loop = False
        else:
            print('Ingrese una opcion correcta.')

    except Exception as e:
        print(e)
