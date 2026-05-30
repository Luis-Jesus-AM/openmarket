import flet as ft

from datetime import datetime

from controller.venta_controller import (
    registrar_venta,
    listar_ventas
)


def vista_pedidos(page: ft.Page):

    PRIMARIO = "#E11D48"
    SECUNDARIO = "#FACC15"
    FONDO = "#FEF2F2"
    GRIS = "#6B7280"

    lista = ft.Column(spacing=10)

    productos_temp = []

    lista_productos_temp = ft.Column(
        spacing=5
    )

    total_temp = ft.Text(

        "Total: $0.00",

        weight="bold",
        color=PRIMARIO
    )

    def actualizar_lista():

        lista.controls.clear()

        ventas = listar_ventas()

        for p in ventas:

            lista.controls.append(

                ft.Card(

                    content=ft.Container(

                        content=ft.Column([

                            ft.Text(
                                p["cliente"],
                                weight="bold"
                            ),

                            ft.Column([

                                ft.Text(

                                    f"{prod['nombre']} x{prod['cantidad']} - ${prod['precio'] * prod['cantidad']:.2f}",

                                    size=12,
                                    color=GRIS

                                )

                                for prod in p["productos"]

                            ]),

                            ft.Text(

                                f"Total: ${sum(prod['precio'] * prod['cantidad'] for prod in p['productos']):.2f}",

                                weight="bold",
                                color=PRIMARIO
                            )

                        ]),

                        padding=15
                    )
                )
            )

        page.update()

    def actualizar_total_temp():

        total = sum(

            prod["precio"] * prod["cantidad"]

            for prod in productos_temp
        )

        total_temp.value = f"Total: ${total:.2f}"

        page.update()

    def agregar_producto(e):

        if (
            producto.value == ""
            or precio.value == ""
            or cantidad.value == ""
        ):
            return

        nuevo = {

            "nombre": producto.value,

            "precio": float(precio.value),

            "cantidad": int(cantidad.value)
        }

        productos_temp.append(nuevo)

        lista_productos_temp.controls.append(

            ft.Text(

                f"{nuevo['nombre']} x{nuevo['cantidad']} - ${nuevo['precio'] * nuevo['cantidad']:.2f}",

                size=12,
                color=GRIS
            )
        )

        producto.value = ""
        precio.value = ""
        cantidad.value = ""

        actualizar_total_temp()

        page.update()

    def finalizar_pedido(e):

        registrado = registrar_venta(

            cliente.value,

            productos_temp,

            str(datetime.now().date())
        )

        if not registrado:
            return

        cliente.value = ""

        productos_temp.clear()

        lista_productos_temp.controls.clear()

        actualizar_total_temp()

        actualizar_lista()

        page.snack_bar = ft.SnackBar(
            ft.Text("Venta registrada")
        )

        page.snack_bar.open = True

        page.update()

    cliente = ft.TextField(

        label="Cliente",

        border_radius=10,

        filled=True
    )

    producto = ft.TextField(

        label="Producto",

        border_radius=10,

        filled=True,

        on_submit=agregar_producto
    )

    precio = ft.TextField(

        label="Precio",

        border_radius=10,

        filled=True,

        keyboard_type=ft.KeyboardType.NUMBER,

        on_submit=agregar_producto
    )

    cantidad = ft.TextField(

        label="Cantidad",

        border_radius=10,

        filled=True,

        keyboard_type=ft.KeyboardType.NUMBER,

        on_submit=agregar_producto
    )

    formulario = ft.Card(

        content=ft.Container(

            content=ft.Column([

                ft.Text(

                    "Registrar venta",

                    size=18,

                    weight="bold",

                    color=PRIMARIO
                ),

                cliente,

                producto,

                precio,

                cantidad,

                ft.Text(

                    "Productos agregados:",

                    weight="bold"
                ),

                lista_productos_temp,

                total_temp,

                ft.Row([

                    ft.ElevatedButton(

                        "Agregar Producto",

                        bgcolor=PRIMARIO,

                        color="white",

                        on_click=agregar_producto
                    ),

                    ft.ElevatedButton(

                        "Finalizar Venta",

                        bgcolor=SECUNDARIO,

                        color="black",

                        on_click=finalizar_pedido
                    )

                ], spacing=10)

            ], spacing=10),

            padding=20,

            width=350
        )
    )

    lista_ventas = ft.Card(

        content=ft.Container(

            content=ft.Column([

                ft.Text(

                    "Ventas recientes",

                    size=18,

                    weight="bold",

                    color=PRIMARIO
                ),

                lista

            ]),

            padding=20,

            expand=True
        )
    )

    actualizar_lista()

    actualizar_total_temp()

    return ft.Container(

        bgcolor=FONDO,

        expand=True,

        padding=20,

        content=ft.Column([

            ft.Text(

                "Pedidos",

                size=30,

                weight="bold",

                color=PRIMARIO
            ),

            ft.Row(

                [
                    formulario,
                    lista_ventas
                ],

                spacing=20,

                expand=True
            )

        ])
    )