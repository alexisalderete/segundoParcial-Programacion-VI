# Importa todas las funciones y clases del módulo 'flet'
from flet import *
# Importa el módulo 'flet' con un alias 'ft' para un acceso más fácil a sus componentes
import flet as ft
# Importa el conector de MySQL para interactuar con la base de datos
import mysql.connector

# Conexión a la base de datos MySQL
mydb = mysql.connector.connect(
    host="localhost",        
    user="root",             
    password="",             
    db="appFlet"             
)
# cursor para ejecutar comandos SQL en la base de datos
cursor = mydb.cursor()

def main(page: ft.Page):
    # Configura el título de la ventana de la aplicación
    page.title = "AlexCompany"
    # Establece el ancho de la ventana
    page.window.width = 400
    # Establece la altura de la ventana
    page.window.height = 680
    # Variable para almacenar el nombre del usuario actual
    usuario_actual = ""

    # Campo de texto para el nombre de usuario en la interfaz de usuario
    nombretxt = TextField(
        label="Nombre de usuario",# Etiqueta del campo de texto
        bgcolor="black",# Color de fondo negro
        color="white",# Color del texto blanco
        border_color="grey",# Color del borde gris
        border_radius=15# Bordes redondeados
    )
    
    # Campo de texto para la contraseña
    clavetxt = TextField(
        label="Contraseña",# Etiqueta del campo de texto
        bgcolor="black",# Color de fondo negro
        color="white",# Color del texto blanco
        border_color="grey",# Color del borde gris
        password=True,# Ocultar el texto como contraseña
        can_reveal_password=True,# Permite mostrar/ocultar contraseña
        border_radius=15# Bordes redondeados
    )
    
    # Función para crear el AppBar con un título dado
    def crear_appbar(titulo):
        return ft.AppBar(
            title=ft.Text(titulo, size=18),# Título del AppBar
            center_title=False,# No centrar el título
            bgcolor=ft.colors.SURFACE_VARIANT,# Color de fondo del AppBar
            actions=[# Acciones en el AppBar
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),   # Botón de tema
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text=usuario_actual, icon= icons.ACCOUNT_CIRCLE, on_click=lambda _: page.go("/")),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(text="Inicio", icon= icons.HOME, on_click=lambda _: page.go("/")),
                        ft.PopupMenuItem(text="Calificaciones", icon=icons.TASK ,  on_click=lambda _: page.go("/calificacion")),
                        ft.PopupMenuItem(text="Registrarse", icon= icons.ADD_ROUNDED, on_click=lambda _: page.go("/registro")),
                        ft.PopupMenuItem(text="Cerrar sesión", icon= icons.LOGOUT, on_click=lambda _: page.go("/login")),
                    ]
                ),
            ],
        )
    
    # Función para manejar la autenticación
    def iniciar_sesion(e):
        nonlocal usuario_actual
        # Obtiene el nombre de usuario y contraseña ingresados
        username, password = nombretxt.value, clavetxt.value
            
        # Verifica que se ingresaron ambos campos
        if username and password:
            # Consulta SQL para verificar si el usuario y contraseña existen
            cursor.execute("SELECT * FROM usuarios WHERE usu_nombre = %s AND usu_clave = %s", (username, password))
            # Si la consulta devuelve un resultado, el usuario existe
            if cursor.fetchone():
                usuario_actual = username        # Guarda el usuario actual
                page.go("/")                     # Redirige a la página principal
                nombretxt.value, clavetxt.value = "", ""  # Limpia los campos de entrada
            else:
                mostrar_alerta("Error inesperado", "Nombre de usuario o contraseña incorrectos.")
        else:
            mostrar_alerta("Error inesperado", "Debes ingresar el nombre de usuario y la contraseña.")
            
        page.update()  # Actualiza la interfaz de usuario
    
    # Función para mostrar un cuadro de alerta
    def mostrar_alerta(titulo, mensaje):
        alerta = ft.AlertDialog(
            modal=True,# Cuadro de diálogo modal
            title=ft.Text(titulo),# Título del cuadro de alerta
            content=ft.Text(mensaje),# Mensaje del cuadro de alerta
            actions=[ft.TextButton("Aceptar", on_click=lambda _: page.close(alerta))],
            actions_alignment=ft.MainAxisAlignment.END,  # Alineación de los botones
        )
        page.overlay.append(alerta)# Añade la alerta a la superposición
        alerta.open = True# Abre el cuadro de alerta
    
    # Función para registrar un nuevo usuario
    def registrar_usuario(e):
        nonlocal usuario_actual
        # Obtiene el nombre de usuario y contraseña ingresados
        nuevo_usuario, nueva_clave = nombre_registro.value, clave_registro.value

        # Verifica que se ingresaron ambos campos
        if nuevo_usuario and nueva_clave:
            # Consulta SQL para verificar si el usuario ya existe
            cursor.execute("SELECT * FROM usuarios WHERE usu_nombre = %s", (nuevo_usuario,))
            if cursor.fetchone():  # Si existe un resultado, el usuario ya está registrado
                mostrar_alerta("Error inesperado", "El usuario ya existe.")
            else:
                # Inserta el nuevo usuario en la base de datos
                cursor.execute("INSERT INTO usuarios (usu_nombre, usu_clave, usu_tipo, usu_estado) VALUES (%s, %s, 'Estudiante', 'Activo')", (nuevo_usuario, nueva_clave))
                mydb.commit()# Confirma la transacción
                usuario_actual = nuevo_usuario# Guarda el usuario actual
                page.go("/")# Redirige a la página principal
                nombre_registro.value, clave_registro.value = "", ""
        else:
            mostrar_alerta("Error inesperado", "Debes ingresar el nombre de usuario y la contraseña.")
        page.update()

    # Contenedor con elementos UI para el login
    contenedor_login = Container(
        content=Column(
            [
                Text("Alex Company", size=32, weight="bold", color="white"),
                Text("Bienvenido", size=24, weight="bold", color="white"),
                Text("Iniciar sesión en Alex Company", size=16, color="white"),
                nombretxt, clavetxt,
                Text("¿Olvidaste tu contraseña?", size=14, color="grey", text_align="center"),
                ElevatedButton(text="Iniciar sesión", bgcolor="white", color="black", width=page.window.width * 0.8, height=35, on_click=iniciar_sesion),
                Text("o", size=16, color="grey"),
                ElevatedButton(text="Iniciar sesión con Apple", icon=icons.APPLE, bgcolor="#171717", color="white", width=page.window.width * 0.8, height=35),
                ElevatedButton(text="Iniciar sesión con teléfono", icon=icons.PHONE, bgcolor="#171717", color="white", width=page.window.width * 0.8, height=35),
                
                Container(
                    content=Text("¿No tienes una cuenta?", size=14, color="grey", text_align="center"),
                    on_click=lambda _: page.go("/registro"),
                ),
            ],
            alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER, spacing=10,
        ),
        bgcolor="black", border_radius=10, alignment=alignment.center, padding=20, width=380, height=600,
    )

    # Campos de texto para el registro
    nombre_registro, clave_registro = TextField(label="Nombre de usuario", bgcolor="black", color="white", border_color="grey", border_radius=15), TextField(label="Contraseña", bgcolor="black", color="white", border_color="grey", password=True, can_reveal_password=True, border_radius=15)
    # Contenedor con elementos UI para el registro
    contenedor_registro = Container(
        content=Column(
            [
                Text("Registro de Usuario", size=32, weight="bold", color="white"),
                nombre_registro, clave_registro,
                ElevatedButton(text="Registrarse", bgcolor="white", color="black", width=page.window.width * 0.8, height=35, on_click=registrar_usuario),
                
                Container(
                    content=Text("¿Ya tienes una cuenta?", size=14, color="grey", text_align="center"),
                    on_click=lambda _: page.go("/login"),
                ),
            ],
            alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER, spacing=10,
        ),
        bgcolor="black", border_radius=10, alignment=alignment.center, padding=20, width=380, height=600,
    )

    # Función para cambiar la vista según la ruta
    def route_change(route):
        page.views.clear() # Limpia las vistas actuales
        if page.route == "/":
            # Vista principal
            page.views.append(
                ft.View(
                    "/",
                    [
                        crear_appbar("AlexCompany"), 
                        Text(f" ¡Buenos días {usuario_actual}!", size=24, color="white"),
                        ft.ElevatedButton("Ver calificación", icon=icons.TASK, on_click=lambda _: page.go("/calificacion"))
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        elif page.route == "/calificacion":
            # Vista de calificación
            page.views.append(
                ft.View(
                    "/calificacion",
                    [
                        crear_appbar("Calificaciones"),
                        ft.ElevatedButton("Ir al Inicio", icon=icons.HOME, on_click=lambda _: page.go("/"))
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        elif page.route == "/login":
            # Vista de login
            page.views.append(
                ft.View(
                    "/login",
                    [
                        contenedor_login
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
        elif page.route == "/registro":
            # Vista de registro
            page.views.append(
                ft.View(
                    "/registro",
                    [
                        contenedor_registro
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )
            
        page.update()  # Actualiza la vista

    # Configura la navegación y ruta inicial
    page.on_route_change, page.on_view_pop = route_change, lambda _: page.views.pop() or page.go(page.views[-1].route)
    page.go("/login")  # Establece la página inicial en login

ft.app(target=main)