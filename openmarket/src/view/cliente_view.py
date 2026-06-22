import flet as ft

from controller.cliente_controller import (
    listar_clientes,
    registrar_cliente
)


def vista_clientes(page: ft.Page):

    VERDE = "#16A34A"
    FONDO = "#F5F7FA"
    GRIS = "#6B7280"

    lista = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=False
    )

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

                                    ft.Text(
                                        c["correo"],
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

                                        ft.Text(
                                            c["correo"],
                                            size=12,
                                            color=GRIS
                                        )
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
        resultado = registrar_cliente(
            nombre.value,
            telefono.value,
            correo.value
        )
        
        print(f"Resultado del registro: {resultado}")
        
        # Diccionario de mensajes
        mensajes = {
            "campos_vacios": "Todos los campos son obligatorios",
            "telefono_invalido": "El teléfono debe tener 10 dígitos",
            "correo_invalido": "Correo electrónico inválido",
            "telefono_existente": "El teléfono ya está registrado",
        }
        
        if resultado in mensajes:
            # ✅ FORMA 1: Con overlay (más confiable)
            snack = ft.SnackBar(
                content=ft.Text(mensajes[resultado]),
                bgcolor="red",
                duration=3000
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()
            
        elif resultado == "ok":
            nombre.value = ""
            telefono.value = ""
            correo.value = ""
            actualizar_lista()
            
            # ✅ SnackBar de éxito
            snack = ft.SnackBar(
                content=ft.Text("Cliente agregado ✅"),
                bgcolor="green",
                duration=3000
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()

    nombre = ft.TextField(
        label="Nombre",
        border_radius=10,
        filled=True
    )

    telefono = ft.TextField(
        label="Teléfono",
        border_radius=10,
        filled=True,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    correo = ft.TextField(
    label="Correo",
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
                correo,

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
        expand=True,

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