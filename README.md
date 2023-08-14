# SISTEMA DE LOGIN Y REGISTRO CON POSTGRESQL

Este repositorio contiene el código fuente de un sistema de gestión de usuarios desarrollado en Python. El sistema permite a los usuarios registrarse, iniciar sesión y, en el caso de los administradores, realizar algunas acciones adicionales.

![Menu](https://cdn.discordapp.com/attachments/1116592460009852971/1139755186865320008/image.png)

## Estructura del Código
El código está organizado en varios archivos que cumplen diferentes funciones:

* **database.py:** Contiene la clase Database que se encarga de manejar la conexión y el cursor a la base de datos PostgreSQL.
* **dao_usuario.py:** Contiene la clase DAOUsuario que implementa la lógica de acceso a la base de datos para las operaciones relacionadas con usuarios.
* **usuario.py:** Define la clase Usuario que modela la estructura de los usuarios y proporciona métodos setter y getter.
* **menu.py:** Implementa un menú interactivo para el inicio de sesión y el registro de usuarios.

## Uso del Código
Para utilizar el sistema, sigue los siguientes pasos:

* Ejecuta el programa **menu.py**.
* Selecciona la opción 1 para iniciar sesión o la opción 2 para registrarte.
* Si eliges registrarte, sigue las indicaciones para ingresar tu nombre de usuario y contraseña.
* Si eliges iniciar sesión, ingresa tu nombre de usuario y contraseña.
* Si inicias sesión como administrador, tendrás opciones adicionales, como crear usuarios administradores y cambiar contraseñas.

## Requisitos y Dependencias
* Python 3.x
* PostgreSQL
* Psycopg2

## Configuración de la Base de Datos
El código asume que tienes una base de datos PostgreSQL configurada con los siguientes detalles:

* Base de datos: sistema_prueba
* Usuario: postgres
* Contraseña: admin
* Host: 127.0.0.1
* Puerto: 5432

Debes tener una tabla llamada usuarios con las siguientes columnas:
* id_user (Serial)
* name_user (Charvar 20)
* pass_user
* is_admin (Check IN ('S','N'))

Si necesitas modificar estos valores, puedes hacerlo en la clase Database del archivo database.py.
