import flet as ft

from controller.corte_controller import (

    calcular_totales,

    obtener_actividad,

    obtener_corte_dia
)


def vista_corte(page: ft.Page):

    MORADO = "#7C3AED"

    VERDE = "#16A34A"

    ROJO = "#DC2626"

    FONDO = "#F5F7FA"

    GRIS = "#6B7280"

    total, cantidad, pendiente = calcular_totales()

    def cerrar_dialog(dialog):

        dialog.open = False

        page.update()

    def corte_del_dia(e):

        total_hoy = obtener_corte_dia()

        dialog = ft.AlertDialog(

            title=ft.Text(

                "Corte del día",

                weight="bold",

                color=MORADO
            ),

            content=ft.Text(

                f"Ganancias de hoy: ${total_hoy:.2f}",

                size=16
            ),

            actions=[

                ft.TextButton(

                    "Cerrar",

                    on_click=lambda e: cerrar_dialog(dialog)
                )

            ]
        )

        page.dialog = dialog

        dialog.open = True

        page.update()

    def card_titulo_valor(

        titulo,
        valor,
        color
    ):

        return ft.Card(

            content=ft.Container(

                content=ft.Column([

                    ft.Text(

                        titulo,

                        size=14,

                        weight="bold"
                    ),

                    ft.Text(

                        valor,

                        size=22,

                        weight="bold",

                        color=color
                    )

                ]),

                padding=20,

                width=200
            )
        )

    actividad_data = obtener_actividad()

    actividad = ft.Column([

        ft.Text(

            f"{p['cliente']} compró {', '.join([prod['nombre'] for prod in p['productos']])} - ${sum(prod['precio'] * prod['cantidad'] for prod in p['productos']):.2f}",

            size=12,

            color=GRIS
        )

        for p in actividad_data

    ])

    return ft.Container(

        bgcolor=FONDO,

        expand=True,

        padding=20,

        content=ft.Column([

            ft.Text(

                "Corte",

                size=30,

                weight="bold",

                color=MORADO
            ),

            ft.Row([

                card_titulo_valor(

                    "Ventas totales",

                    f"${total:.2f}",

                    MORADO
                ),

                card_titulo_valor(

                    "Pedidos",

                    f"{cantidad}",

                    VERDE
                ),

                card_titulo_valor(

                    "Pendiente",

                    f"${pendiente:.2f}",

                    ROJO
                ),

            ], spacing=20),

            ft.Divider(),

            ft.ElevatedButton(

                "Corte del día",

                bgcolor=MORADO,

                color="white",

                style=ft.ButtonStyle(

                    shape=ft.RoundedRectangleBorder(
                        radius=10
                    )
                ),

                on_click=corte_del_dia
            ),

            ft.Divider(),

            ft.Card(

                content=ft.Container(

                    content=ft.Column([

                        ft.Text(

                            "Actividad reciente",

                            size=18,

                            weight="bold",

                            color=MORADO
                        ),

                        actividad

                    ]),

                    padding=20
                )
            )

        ])
    )