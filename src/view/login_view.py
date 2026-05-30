import flet as ft

from view.dashboard_view import vista_dashboard


def vista_login(page: ft.Page):

    VERDE = "#16A34A"

    FONDO = "#F5F7FA"

    GRIS = "#6B7280"

    BLANCO = "#FFFFFF"

    def iniciar_sesion(e):

        if usuario.value == "" or password.value == "":

            page.snack_bar = ft.SnackBar(
                ft.Text("Completa todos los campos")
            )

            page.snack_bar.open = True

            page.update()

            return

        page.clean()

        page.add(
            vista_dashboard(page)
        )

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

        label="Usuario",

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

                boton_login

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