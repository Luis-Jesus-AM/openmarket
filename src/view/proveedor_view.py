import flet as ft

from controller.proveedor_controller import (

    listar_proveedores,

    registrar_proveedor
)


def vista_proveedores(page: ft.Page):

    VERDE = "#16A34A"

    FONDO = "#F5F7FA"

    GRIS = "#6B7280"

    lista = ft.Column(
        spacing=10
    )

    def actualizar_lista():

        lista.controls.clear()

        proveedores = listar_proveedores()

        for p in proveedores:

            lista.controls.append(

                ft.Card(

                    content=ft.Container(

                        content=ft.Row(

                            [

                                ft.Column([

                                    ft.Text(

                                        p["empresa"],

                                        weight="bold"
                                    ),

                                    ft.Text(

                                        p["contacto"],

                                        size=12,

                                        color=GRIS
                                    ),

                                    ft.Text(

                                        p["telefono"],

                                        size=12,

                                        color=GRIS
                                    ),

                                ]),

                                ft.Icon(

                                    ft.Icons.WORK,

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

    def agregar_nuevo_proveedor(e):

        registrado = registrar_proveedor(

            empresa.value,

            contacto.value,

            telefono.value
        )

        if not registrado:
            return

        empresa.value = ""

        contacto.value = ""

        telefono.value = ""

        actualizar_lista()

        page.snack_bar = ft.SnackBar(
            ft.Text("Proveedor agregado")
        )

        page.snack_bar.open = True

        page.update()

    empresa = ft.TextField(

        label="Empresa",

        border_radius=10,

        filled=True
    )

    contacto = ft.TextField(

        label="Contacto",

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

                    "Registrar proveedor",

                    size=18,

                    weight="bold"
                ),

                empresa,

                contacto,

                telefono,

                ft.ElevatedButton(

                    "Agregar Proveedor",

                    bgcolor=VERDE,

                    color="white",

                    style=ft.ButtonStyle(

                        shape=ft.RoundedRectangleBorder(
                            radius=10
                        )
                    ),

                    on_click=agregar_nuevo_proveedor
                )

            ], spacing=10),

            padding=20,

            width=350
        )
    )

    lista_proveedores = ft.Card(

        content=ft.Container(

            content=ft.Column([

                ft.Text(

                    "Proveedores registrados",

                    size=18,

                    weight="bold"
                ),

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

                "Proveedores",

                size=30,

                weight="bold"
            ),

            ft.Row(

                [
                    formulario,
                    lista_proveedores
                ],

                spacing=20,

                expand=True
            )

        ])
    )