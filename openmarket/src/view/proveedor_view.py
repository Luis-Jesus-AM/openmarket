import flet as ft

from controller.proveedor_controller import (
    listar_proveedores,
    registrar_proveedor
)


def vista_proveedores(page: ft.Page):

    VERDE = "#16A34A"
    FONDO = "#F5F7FA"
    GRIS = "#6B7280"

    lista = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=False
    )

    # Barra de búsqueda
    busqueda = ft.TextField(
        label="Buscar proveedor",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=10,
        filled=True,
        on_change=lambda e: filtrar_lista()
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
                                    ft.Text(p["nombre"] or "Sin nombre", weight="bold"),
                                    ft.Text(p["correo"] or "Sin correo", size=12, color=GRIS),
                                    ft.Text(p["telefono"] or "Sin teléfono", size=12, color=GRIS),
                                    ft.Text(p["producto_que_vende"] or "Sin producto", size=12, color=GRIS),
                                ]),
                                ft.Icon(ft.Icons.WORK, color=VERDE)
                            ],
                            alignment="spaceBetween"
                        ),
                        padding=15
                    )
                )
            )
        page.update()

    def filtrar_lista():
        texto = busqueda.value.strip().lower()
        lista.controls.clear()
        proveedores = listar_proveedores()

        for p in proveedores:
            nombre_p = p["nombre"] or ""
            correo_p = p["correo"] or ""
            telefono_p = p["telefono"] or ""
            producto_p = p["producto_que_vende"] or ""

            if (texto in nombre_p.lower() or 
                texto in correo_p.lower() or 
                texto in telefono_p.lower() or 
                texto in producto_p.lower()):
                
                lista.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row(
                                [
                                    ft.Column([
                                        ft.Text(p["nombre"] or "Sin nombre", weight="bold"),
                                        ft.Text(p["correo"] or "Sin correo", size=12, color=GRIS),
                                        ft.Text(p["telefono"] or "Sin teléfono", size=12, color=GRIS),
                                        ft.Text(p["producto_que_vende"] or "Sin producto", size=12, color=GRIS),
                                    ]),
                                    ft.Icon(ft.Icons.WORK, color=VERDE)
                                ],
                                alignment="spaceBetween"
                            ),
                            padding=15
                        )
                    )
                )
        page.update()

    nombre = ft.TextField(label="Nombre del proveedor", border_radius=10, filled=True)
    correo = ft.TextField(label="Correo", border_radius=10, filled=True)
    telefono = ft.TextField(label="Teléfono", border_radius=10, filled=True, keyboard_type=ft.KeyboardType.NUMBER)
    producto_que_vende = ft.TextField(label="Producto que vende", border_radius=10, filled=True)
    direccion = ft.TextField(label="Dirección", border_radius=10, filled=True)

    def agregar_nuevo_proveedor(e):
        registrado = registrar_proveedor(
            nombre.value, correo.value, telefono.value, producto_que_vende.value, direccion.value
        )
        if not registrado:
            snack_error = ft.SnackBar(
                content=ft.Text("⚠ Error: Verifica que los campos obligatorios no estén vacíos"),
                bgcolor="red", duration=3000
            )
            page.overlay.append(snack_error)
            snack_error.open = True
            page.update()
            return
        nombre.value = ""
        correo.value = ""
        telefono.value = ""
        producto_que_vende.value = ""
        direccion.value = ""
        actualizar_lista()
        snack_exito = ft.SnackBar(
            content=ft.Text("✅ Proveedor agregado con éxito"),
            bgcolor="green", duration=3000
        )
        page.overlay.append(snack_exito)
        snack_exito.open = True
        page.update()

    formulario = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Registrar proveedor", size=18, weight="bold"),
                nombre, correo, telefono, producto_que_vende, direccion,
                ft.ElevatedButton(
                    "Agregar Proveedor", bgcolor=VERDE, color="white",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=agregar_nuevo_proveedor
                )
            ], spacing=10),
            padding=20, width=350
        )
    )

    lista_proveedores = ft.Card(
        expand=True,
        content=ft.Container(
            content=ft.Column([
                ft.Text("Proveedores registrados", size=18, weight="bold"),
                busqueda,
                lista
            ], expand=True),
            padding=20, expand=True
        )
    )

    actualizar_lista()

    return ft.Container(
        bgcolor=FONDO, expand=True, padding=20,
        content=ft.Column([
            ft.Text("Proveedores", size=30, weight="bold"),
            ft.Row([formulario, lista_proveedores], spacing=20, expand=True)
        ])
    )