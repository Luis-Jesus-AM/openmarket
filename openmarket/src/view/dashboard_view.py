import flet as ft

from view.cliente_view import vista_clientes
from view.proveedor_view import vista_proveedores
from view.ventas_view import vista_pedidos
from view.corte_view import vista_corte
from view.producto_view import vista_productos


def vista_dashboard(page: ft.Page):

    VERDE = "#16A34A"
    FONDO = "#F5F7FA"
    BLANCO = "#FFFFFF"

    contenido = ft.Container(
        expand=True,
        padding=20,
        bgcolor=FONDO
    )

    def cambiar_vista(vista):
        contenido.content = vista(page)
        page.update()

    def cerrar_sesion(e):
        from view.login_view import vista_login
        page.clean()
        page.add(vista_login(page))
        page.update()  

    sidebar = ft.Container(
        width=230,
        bgcolor=BLANCO,
        padding=20,
        content=ft.Column([
            ft.Row([
                ft.Icon(
                    ft.Icons.STORE,
                    color=VERDE,
                    size=35
                ),
                ft.Text(
                    "OpenMarket",
                    size=24,
                    weight="bold",
                    color=VERDE
                )
            ], spacing=10),

            ft.Divider(),

            ft.ElevatedButton(
                "Ventas",
                icon=ft.Icons.POINT_OF_SALE,
                width=180,
                bgcolor=VERDE,
                color="white",
                on_click=lambda e: cambiar_vista(vista_pedidos)
            ),

            ft.ElevatedButton(
                "Productos",
                icon=ft.Icons.INVENTORY_2,
                width=180,
                on_click=lambda e: cambiar_vista(vista_productos)
            ),

            ft.ElevatedButton(
                "Clientes",
                icon=ft.Icons.PEOPLE,
                width=180,
                on_click=lambda e: cambiar_vista(vista_clientes)
            ),

            ft.ElevatedButton(
                "Proveedores",
                icon=ft.Icons.WORK,
                width=180,
                on_click=lambda e: cambiar_vista(vista_proveedores)
            ),

            ft.ElevatedButton(
                "Corte",
                icon=ft.Icons.ANALYTICS,
                width=180,
                on_click=lambda e: cambiar_vista(vista_corte)
            ),

            ft.Divider(),

            ft.ElevatedButton(
                "Cerrar sesión",
                icon=ft.Icons.LOGOUT,
                width=180,
                bgcolor="#DC2626",
                color="white",
                on_click=cerrar_sesion  
            )
        ], spacing=15)
    )

    contenido.content = vista_pedidos(page)

    return ft.Container(
        expand=True,
        bgcolor=FONDO,
        content=ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=1, color="#E5E7EB"), 
                contenido
            ],
            expand=True,
            spacing=0
        )
    )