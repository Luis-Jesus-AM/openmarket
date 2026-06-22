import flet as ft

from view.dashboard_view import vista_dashboard
from view.registro_view import vista_registro 
from controller.login_controller import validar_login

import config

def vista_login(page: ft.Page):

    VERDE = "#16A34A"
    FONDO = "#F5F7FA"
    GRIS = "#6B7280"
    BLANCO = "#FFFFFF"

    def iniciar_sesion(e):
        # 1. Validación rápida de campos vacíos en la vista
        if usuario.value == "" or password.value == "":
            mostrar_mensaje("Completa todos los campos", "red")
            return

        resultado = validar_login(usuario.value, password.value)

        # 2. Controlar las respuestas del controlador
        if resultado == "campos_vacios":
            mostrar_mensaje("Llena todos los campos", "red")
            return
        elif resultado == "no_existe":
            mostrar_mensaje("Usuario no existe", "red")
            return
        elif resultado == "password_incorrecto":
            mostrar_mensaje("Contraseña incorrecta", "red")
            return
        
        # 3. Caso Exitoso (Viene un diccionario con los datos del usuario)
        if isinstance(resultado, dict) and "id" in resultado:
            mostrar_mensaje(f"Bienvenido {resultado['nombre']} ✅", "green")
            
            # Guardamos la sesión global
            config.USUARIO_CONECTADO_ID = resultado["id"]
            
            # Limpiamos y cargamos el dashboard
            page.clean()
            page.add(vista_dashboard(page))
            page.update()


    # Función auxiliar para pintar los SnackBars usando el Overlay moderno
    def mostrar_mensaje(texto, color_fondo):
        snack = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=color_fondo,
            duration=3000
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()


    def ir_a_registro(e):
        page.clean()  
        page.add(vista_registro(page))  
        page.update()

    titulo = ft.Column([
        ft.Icon(
            ft.Icons.STORE,
            size=70,
            color=VERDE
        ),
        ft.Text(
            "OpenMarket",
            size=32,
            weight="bold",
            color=VERDE
        ),
        ft.Text(
            "Sistema para emprendedores",
            size=14,
            color=GRIS
        )
    ],
    horizontal_alignment="center",
    spacing=10
    )

    usuario = ft.TextField(
        label="Usuario / Correo", 
        prefix_icon=ft.Icons.PERSON,
        border_radius=12,
        filled=True,
        bgcolor="white"
    )

    password = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        border_radius=12,
        filled=True,
        bgcolor="white"
    )

    boton_login = ft.ElevatedButton(
        "Iniciar sesión",
        width=300,
        height=45,
        bgcolor=VERDE,
        color="white",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(
                radius=12
            )
        ),
        on_click=iniciar_sesion
    )

    enlace_registro = ft.TextButton(
        "¿No tienes cuenta? Regístrate aquí", 
        style=ft.ButtonStyle(color=VERDE),
        on_click=ir_a_registro
    )

    formulario = ft.Card(
        elevation=8,
        content=ft.Container(
            width=380,
            bgcolor=BLANCO,
            border_radius=20,
            padding=30,
            content=ft.Column([
                titulo,
                ft.Divider(height=20, color="transparent"),
                usuario,
                password,
                ft.Divider(height=10, color="transparent"),
                boton_login,
                enlace_registro 
            ],
            horizontal_alignment="center",
            spacing=15)
        )
    )

    return ft.Container(
        expand=True,
        bgcolor=FONDO,
        alignment=ft.Alignment(0, 0),
        content=ft.Row([
            formulario
        ],
        alignment="center")
    )