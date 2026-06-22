import flet as ft

from controller.corte_controller import (
    calcular_totales,
    obtener_actividad,
    obtener_corte_dia,
    listar_cortes_por_periodo  
)

def vista_corte(page: ft.Page):
    MORADO = "#7C3AED"
    VERDE = "#16A34A"
    ROJO = "#DC2626"
    FONDO = "#F5F7FA"
    GRIS = "#6B7280"
    
    total, cantidad, pendiente = calcular_totales()
    
    def cargar_datos():
        return calcular_totales()

    def cerrar_dialog(dialog):
        dialog.open = False
        page.update()

    def corte_del_dia(e):
        total_hoy = obtener_corte_dia()
        if not total_hoy:
            total_hoy = 0
        dialog = ft.AlertDialog(
            title=ft.Text("Corte del día", weight="bold", color=MORADO),
            content=ft.Text(f"Ganancias de hoy: ${total_hoy:.2f}", size=16),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog))
            ]
        ) 
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def mostrar_historial(e):
        lista_filas = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=8)

        def actualizar_vista_historial():
            lista_filas.controls.clear()
            
            tipo = selector_tipo.value
            periodo = selector_especifico.value
            
            if tipo == "todas":
                ventas = listar_cortes_por_periodo("todas", None)
            else:
                if not periodo: 
                    return
                ventas = listar_cortes_por_periodo(tipo, int(periodo))
            
            if not ventas:
                lista_filas.controls.append(
                    ft.Text("No hay ventas en el periodo seleccionado.", color=GRIS, size=13)
                )
            else:
                for v in ventas:
                    lista_filas.controls.append(
                        ft.Text(f"Venta #{v['id_venta']} - ${v['total']:.2f} - {v['fecha_venta']}", size=13)
                    )
            page.update()

        selector_especifico = ft.Dropdown(
            width=150,
            height=40,
            text_size=12,
            visible=False, 
            on_select=lambda e: actualizar_vista_historial()
        )

        def cambiar_tipo_filtro(e):
            tipo = selector_tipo.value
            selector_especifico.options.clear()
            
            if tipo == "todas":
                selector_especifico.visible = False
                actualizar_vista_historial()
            
            elif tipo == "semana":
                selector_especifico.visible = True
                selector_especifico.options = [
                    ft.dropdown.Option(str(i), f"Semana {i}") for i in range(1, 53)
                ]
                selector_especifico.value = "1"
                actualizar_vista_historial()
                
            elif tipo == "mes":
                selector_especifico.visible = True
                meses = [
                    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
                ]
                selector_especifico.options = [
                    ft.dropdown.Option(str(i+1), mes) for i, mes in enumerate(meses)
                ]
                selector_especifico.value = "1"
                actualizar_vista_historial()
                
            page.update()

        selector_tipo = ft.Dropdown(
            width=140,
            height=40,
            text_size=12,
            value="todas",
            options=[
                ft.dropdown.Option("todas", "Todas"),
                ft.dropdown.Option("semana", "Por Semana"),
                ft.dropdown.Option("mes", "Por Mes"),
            ],
            on_select=cambiar_tipo_filtro
        )

        contenido = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Ver:", size=12, color=GRIS, weight="bold"),
                            selector_tipo,
                            selector_especifico 
                        ],
                        alignment="start",
                        spacing=10
                    ),
                    ft.Divider(height=10, color="#E5E7EB"),
                    ft.Container(content=lista_filas, expand=True)
                ]
            ), 
            height=400,
            width=450
        ) 

        dialog = ft.AlertDialog(
            title=ft.Text("Historial de Ventas 2026", weight="bold", color=MORADO),
            content=contenido,
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialog(dialog))
            ]
        )

        page.overlay.append(dialog)
        dialog.open = True

        actualizar_vista_historial()

    def card_titulo_valor(titulo, valor, color):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(titulo, size=14, weight="bold"),
                    ft.Text(valor, size=22, weight="bold", color=color)
                ]),
                padding=20,
                width=200
            )
        )

    actividad_data = obtener_actividad()
    
    if not actividad_data:
        lista_actividad_controles = [ft.Text("Sin movimientos en las últimas 24 horas.", color=GRIS, size=12)]
    else:
        lista_actividad_controles = [
            ft.Text(
                f"Venta #{p['id_venta']} - ${p['total']:.2f} - {p['fecha_venta']}",
                size=12,
                color=GRIS
            )
            for p in actividad_data
        ]

    actividad = ft.Column(lista_actividad_controles, spacing=5)


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
                card_titulo_valor("Ventas totales", f"${total:.2f}", MORADO),
                card_titulo_valor("Pedidos", f"{cantidad}", VERDE),
                card_titulo_valor("Pendiente", f"${pendiente:.2f}", ROJO),
            ], spacing=20),
            
            ft.Divider(),
            
            ft.ElevatedButton(
                "Corte del día",
                bgcolor=MORADO,
                color="white",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10)
                ),
                on_click=corte_del_dia
            ),
            
            ft.Divider(),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        "Actividad reciente",
                                        size=18,
                                        weight="bold",
                                        color=MORADO
                                    ),
                                    ft.ElevatedButton(
                                        "Historial",
                                        on_click=mostrar_historial,
                                    )
                                ],
                                alignment="spaceBetween"
                            ),
                            ft.Divider(height=10, color="#F3F4F6"),
                            actividad 
                        ]
                    ),
                    padding=20
                )
            )
        ], scroll=ft.ScrollMode.AUTO)  
    )