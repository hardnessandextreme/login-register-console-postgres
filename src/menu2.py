import time
from dao_usuario import DAOUsuario, Usuario
from registros.logs import log


def opcionesPanel(usuario, usuarioAdmin):
    if not usuarioAdmin:
        menu = ('1. Cambiar tu contraseña\n'
                '2. Ver tu nombre\n'
                '3. Salir')
    else:
        menu = ('1. Crear usuario administrador\n'
                '2. Cambiar tu contraseña\n'
                '3. Ver tu nombre\n'
                '4. Salir')
    while True:
        time.sleep(0.10)
        print(menu)
        opcion = obtener_opcion_valida('Elige una opción: ', [str(i) for i in range(1, 5)])
        try:
            if opcion == '1' and usuarioAdmin:
                listar_usuarios()
                name_user = input('Ingrese el ID del usuario a convertir a admin: ')
                user = Usuario(name_user=name_user)
                if DAOUsuario.convertirAdmin(user):
                    log.debug(
                        f'(ID: {usuario.id_user}) {usuario.name_user} ha dado rango admin a (ID: {user.id_user})'
                        f' {user.name_user}')
                else:
                    print('El usuario no existe.')

            elif opcion == '2' and usuarioAdmin:
                cambiar_contrasena(usuario)

            elif opcion == '3' and usuarioAdmin:
                print(f'Estas viendo tu nombre: {usuario.name_user}')

            elif opcion == '4' and usuarioAdmin:
                print(f' Cerrando sesión {usuario.name_user} '.center(50, '-'))
                break

            elif opcion == '1':
                print('Vas a cambiar tu contraseña')

            elif opcion == '2':
                print(f'Estas viendo tu nombre: {usuario.name_user}')

            elif opcion == '3':
                print(f' Cerrando sesión {usuario.name_user} '.center(50, '-'))
                break

            else:
                print('Opción inválida, intenta de nuevo.')
        except Exception as exe:
            print(exe)


def cambiar_contrasena(usuario):
    print('Vas a cambiar tu contraseña')
    print('Consejos:\n'
          '1. La contraseña debe tener al menos 8 caracteres, incluyendo: 1 número, 1 letra mayúscula.\n'
          '2. La contraseña no debe exceder los 20 caracteres.\n'
          '3. La confirmación de la contraseña debe ser igual a la contraseña.\n')
    contrasenia_actual = input('Ingrese su contraseña actual: ')
    contrasnia_a_cambiar = input('Ingrese la contraseña nueva: ')
    conf_contrasnia_a_cambiar = input('Confirme la contraseña nueva: ')

    validacion_pass = validar_contrasena(contrasenia_a_cambiar, conf_contrasnia_a_cambiar)

    if contrasnia_a_cambiar != conf_contrasnia_a_cambiar:
        print('La nueva confirmación de la contraseña no es igual.')
    elif validacion_pass:
        print('No cumples con las indicaciones')
    else:
        DAOUsuario.cambiarContrasenia(usuario, contrasenia_actual, conf_contrasnia_a_cambiar)


def validar_contrasena(contrasenia, confirmacion):
    pass_no_tiene_numero = not any(c.isdigit() for c in contrasenia)
    pass_no_tiene_mayus = not any(c.isupper() for c in contrasenia)
    pass_no_conf_pass = contrasenia != confirmacion
    pass_excede_limite = len(contrasenia) > 20
    pass_no_supera_minimo = not len(contrasenia) >= 8

    return (
            pass_no_tiene_numero or pass_no_tiene_mayus or
            pass_no_conf_pass or pass_excede_limite or
            pass_no_supera_minimo
    )


def listar_usuarios():
    listado = DAOUsuario.listarUsuarios()
    for usersLista in listado:
        print(usersLista)


def obtener_opcion_valida(mensaje, opciones_validas):
    while True:
        opcion = input(mensaje)
        if opcion in opciones_validas:
            return opcion
        else:
            print('Opción inválida, intenta de nuevo.')


def iniciarSesion():
    print('-' * 50)
    print('{:^50}'.format(f'Inicio de Sesión'))
    print('-' * 50)
    name_user = input('Ingrese su usuario: ')
    contra = input('Ingrese su contraseña: ')

    if not name_user or not contra:
        print('Rellene todos los campos')
        return

    usuario = Usuario(name_user=name_user, pass_user=contra)
    usuarioDAO = DAOUsuario.logearUsuario(usuario)

    if usuarioDAO:
        print('-' * 50)
        print('{:^50}'.format(f' Bienvenido al sistema {usuario.name_user} '))
        print('-' * 50)
        usuarioAdmin = DAOUsuario.esAdministrador(usuario)
        opcionesPanel(usuario, usuarioAdmin)


def registrarUsuario():
    try:
        print('-' * 50)
        print('{:^50}'.format('Registro de usuario'))
        print('-' * 50)
        print('Consejos:\n'
              '1. El usuario debe tener al menos 3 caracteres y como máximo 20.\n'
              '2. La contraseña debe tener al menos 8 caracteres, incluyendo: 1 número, 1 letra mayúscula.\n'
              '3. La contraseña no debe exceder los 20 caracteres.'
              '4. La confirmación de la contraseña debe ser igual a la contraseña.\n')
        print('-' * 50)
        name_user = input('Ingrese su usuario: ')
        pass_user = input('Ingrese su contraseña: ')
        conf_pass_user = input('Confirme su contraseña: ')

        validacion_pass = validar_registro(name_user, pass_user, conf_pass_user)

        if validacion_pass:
            print('Error: lee las indicaciones.')
        else:
            usuario = Usuario(name_user=name_user, pass_user=pass_user)
            DAOUsuario.registrarUsuario(usuario)
    except Exception as exe:
        print(exe)


def validar_registro(usuario, contrasenia, confirmacion):
    longitud_usuario = len(usuario) < 3 or len(usuario) > 20
    usuario_igual_pass = contrasenia == usuario
    validacion_pass = validar_contrasena(contrasenia, confirmacion)

    return longitud_usuario or usuario_igual_pass or validacion_pass


def main():
    loop = True

    while loop:
        print('-' * 50)
        print('{:^50}'.format('Menu'))
        print('-' * 50)
        print('1. Iniciar Sesión\n'
              '2. Registrarse\n'
              '3. Salir')

        try:
            choice = obtener_opcion_valida('Ingrese una opción: ', ['1', '2', '3'])

            if choice == '1':
                iniciarSesion()
            elif choice == '2':
                registrarUsuario()
            elif choice == '3':
                print(' Saliendo del sistema '.center(50, '-'))
                loop = False
            else:
                print('Ingrese una opción correcta.')

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
