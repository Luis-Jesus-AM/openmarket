import flet as ft

from controller.cliente_controller import (
    listar_clientes,
    registrar_cliente
)


def vista_clientes(page: ft.Page):

    VERDE = "#16A34A"
    FONDO = "#F5F7FA"
    GRIS = "#6B7280"

    lista = ft.Column(spacing=10)

    busqueda = ft.TextField(
        label="Buscar cliente",
        border_radius=10,
        filled=True,
        on_change=lambda e: filtrar_lista()
    )

    def actualizar_lista():

        lista.controls.clear()

        clientes = listar_clientes()

        for c in clientes:

            lista.controls.append(

                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.Column([
                                    ft.Text(
                                        c["nombre"],
                                        weight="bold"
                                    ),

                                    ft.Text(
                                        c["telefono"],
                                        size=12,
                                        color=GRIS
                                    ),
                                ]),

                                ft.Icon(
                                    ft.Icons.PERSON,
                                    color=VERDE
                                )
                            ],

                            alignment="spaceBetween"
                        ),

                        padding=15
                    )
                )
            )

        page.update()

    def filtrar_lista():

        texto = busqueda.value.lower()

        lista.controls.clear()

        clientes = listar_clientes()

        for c in clientes:

            if texto in c["nombre"].lower():

                lista.controls.append(

                    ft.Card(
                        content=ft.Container(
                            content=ft.Row(
                                [
                                    ft.Column([
                                        ft.Text(
                                            c["nombre"],
                                            weight="bold"
                                        ),

                                        ft.Text(
                                            c["telefono"],
                                            size=12,
                                            color=GRIS
                                        ),
                                    ]),

                                    ft.Icon(
                                        ft.Icons.PERSON,
                                        color=VERDE
                                    )
                                ],

                                alignment="spaceBetween"
                            ),

                            padding=15
                        )
                    )
                )

        page.update()

    def agregar_cliente(e):

        registrado = registrar_cliente(

            nombre.value,
            telefono.value
        )

        if not registrado:
            return

        nombre.value = ""
        telefono.value = ""

        actualizar_lista()

        page.snack_bar = ft.SnackBar(
            ft.Text("Cliente agregado")
        )

        page.snack_bar.open = True

        page.update()

    nombre = ft.TextField(
        label="Nombre",
        border_radius=10,
        filled=True
    )

    telefono = ft.TextField(
        label="Teléfono",
        border_radius=10,
        filled=True
    )

    formulario = ft.Card(

        content=ft.Container(

            content=ft.Column([

                ft.Text(
                    "Registrar cliente",
                    size=18,
                    weight="bold"
                ),

                nombre,
                telefono,

                ft.ElevatedButton(

                    "Agregar Cliente",

                    bgcolor=VERDE,
                    color="white",

                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(
                            radius=10
                        )
                    ),

                    on_click=agregar_cliente
                )

            ], spacing=10),

            padding=20,
            width=350
        )
    )

    lista_clientes = ft.Card(

        content=ft.Container(

            content=ft.Column([

                ft.Text(
                    "Clientes registrados",
                    size=18,
                    weight="bold"
                ),

                busqueda,

                lista

            ]),

            padding=20,
            expand=True
        )
    )

    actualizar_lista()

    return ft.Container(

        bgcolor=FONDO,
        expand=True,
        padding=20,

        content=ft.Column([

            ft.Text(
                "Clientes",
                size=30,
                weight="bold"
            ),

            ft.Row(

                [
                    formulario,
                    lista_clientes
                ],

                spacing=20,
                expand=True
            )
        ])
    )