import flet as ft

from controller.producto_controller import (

    registrar_producto,

    listar_productos
)


def vista_productos(page: ft.Page):

    AZUL = "#2563EB"

    FONDO = "#F5F7FA"

    GRIS = "#6B7280"

    lista = ft.Column(
        spacing=10
    )

    productos_temp = []

    def actualizar_lista():

        lista.controls.clear()

        for p in productos_temp:

            lista.controls.append(

                ft.Card(

                    content=ft.Container(

                        content=ft.Row(

                            [

                                ft.Column([

                                    ft.Text(

                                        p["nombre"],

                                        weight="bold"
                                    ),

                                    ft.Text(

                                        f"Precio: ${p['precio']}",

                                        size=12,

                                        color=GRIS
                                    ),

                                    ft.Text(

                                        f"Stock: {p['stock']}",

                                        size=12,

                                        color=GRIS
                                    )

                                ]),

                                ft.Icon(

                                    ft.Icons.INVENTORY_2,

                                    color=AZUL
                                )

                            ],

                            alignment="spaceBetween"
                        ),

                        padding=15
                    )
                )
            )

        page.update()

    def agregar_producto(e):

        registrado = registrar_producto(

            nombre.value,

            precio.value,

            stock.value
        )

        if not registrado:
            return

        productos_temp.append({

            "nombre": nombre.value,

            "precio": precio.value,

            "stock": stock.value
        })

        nombre.value = ""

        precio.value = ""

        stock.value = ""

        actualizar_lista()

        page.snack_bar = ft.SnackBar(
            ft.Text("Producto agregado")
        )

        page.snack_bar.open = True

        page.update()

    nombre = ft.TextField(

        label="Nombre",

        border_radius=10,

        filled=True
    )

    precio = ft.TextField(

        label="Precio",

        border_radius=10,

        filled=True,

        keyboard_type=ft.KeyboardType.NUMBER
    )

    stock = ft.TextField(

        label="Stock",

        border_radius=10,

        filled=True,

        keyboard_type=ft.KeyboardType.NUMBER
    )

    formulario = ft.Card(

        content=ft.Container(

            content=ft.Column([

                ft.Text(

                    "Registrar producto",

                    size=18,

                    weight="bold"
                ),

                nombre,

                precio,

                stock,

                ft.ElevatedButton(

                    "Agregar Producto",

                    bgcolor=AZUL,

                    color="white",

                    style=ft.ButtonStyle(

                        shape=ft.RoundedRectangleBorder(
                            radius=10
                        )
                    ),

                    on_click=agregar_producto
                )

            ], spacing=10),

            padding=20,

            width=350
        )
    )

    lista_productos = ft.Card(

        content=ft.Container(

            content=ft.Column([

                ft.Text(

                    "Productos registrados",

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

                "Productos",

                size=30,

                weight="bold",

                color=AZUL
            ),

            ft.Row(

                [
                    formulario,
                    lista_productos
                ],

                spacing=20,

                expand=True
            )

        ])
    )