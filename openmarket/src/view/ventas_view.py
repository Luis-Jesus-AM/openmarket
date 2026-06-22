import flet as ft
from datetime import datetime
from controller.venta_controller import (
    registrar_venta,
    listar_ventas
)
from controller.cliente_controller import (
    registrar_cliente
)
from model.cliente_model import (
    existe_cliente
)
from controller.producto_controller import (
    listar_productos
)

def vista_pedidos(page: ft.Page):

    PRIMARIO = "#E11D48"
    SECUNDARIO = "#FACC15"
    FONDO = "#FEF2F2"
    GRIS = "#6B7280"

    lista = ft.ListView(
        expand=True,
        spacing=10,
    )
    productos_temp = []
    productos_db = listar_productos()
    lista_productos_temp = ft.Column(
        spacing=5
    )
    sugerencias_productos = ft.Column(
        spacing=2
    )
    total_temp = ft.Text(
        "Total: $0.00",
        size=28,
        weight="bold",
        color=PRIMARIO
    )

    def actualizar_lista():
        lista.controls.clear()
        ventas = listar_ventas()
        
        for p in ventas:
            componentes_productos = []
            
            if "productos" in p and p["productos"]:
                for prod in p["productos"]:
                    nombre = prod.get("nombre", "Producto")
                    cant = prod.get("cantidad", 0)
                    
                    # --- CORREGIDO PARA EL NUEVO MODELO ---
                    # Extraemos la unidad que viene mapeada desde el historial de ventas
                    uni = f" {prod.get('unidad', '')}" if prod.get('unidad') else ""
                    
                    precio_u = prod.get("precio", prod.get("precio_unitario", 0))
                    sub = precio_u * cant
                    
                    componentes_productos.append(
                        ft.Row(
                            [
                                ft.Text(
                                    nombre, 
                                    size=12, 
                                    color=GRIS, 
                                    expand=True,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                                # Ampliamos el width a 55 para que quepa la cantidad junto con su unidad (ej: x3 Kg)
                                ft.Text(f"x{cant}{uni}", size=12, color=GRIS, width=55, text_align="center"),
                                ft.Text(f"${sub:.2f}", size=12, color=GRIS, width=65, text_align="right")
                            ],
                            spacing=5
                        )
                    )
            else:
                componentes_productos.append(
                    ft.Text("Sin productos registrados", size=12, color="red")
                )

            lista.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(p.get("cliente", "Desconocido"), weight="bold"),
                            ft.Column(componentes_productos, spacing=4), 
                            ft.Divider(height=1, color="#E5E7EB"),
                            ft.Text(
                                f"Total: ${p.get('total', 0.0):.2f}",
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
    
    def reconstruir_ticket():
        lista_productos_temp.controls.clear()
        for i, prod in enumerate(productos_temp):
            subtotal_prod = prod['precio'] * prod['cantidad']
            uni = f" {prod['unidad']}" if prod.get('unidad') else ""
                    
            lista_productos_temp.controls.append(
                ft.Row(
                    [
                        ft.Text(
                            prod['nombre'], 
                            size=12, 
                            expand=True,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS
                        ),
                        ft.Text(
                            f"${prod['precio']:.2f}", 
                            size=12, 
                            width=55, 
                            text_align="right"
                        ),
                        # --- CORREGIDO: Muestra la cantidad y unidad en el ticket activo ---
                        ft.Text(
                            f"{prod['cantidad']}{uni}", 
                            size=12, 
                            width=60, 
                            text_align="center",
                            weight="w500"
                        ),
                        ft.Text(
                            f"${subtotal_prod:.2f}", 
                            size=12, 
                            width=65, 
                            text_align="right",
                            weight="bold"
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="red",
                            icon_size=18,
                            width=40,
                            tooltip="Eliminar",
                            on_click=lambda e, idx=i: eliminar_producto(idx)
                        )
                    ],
                    spacing=5,
                    alignment="center"
                )
            )

    def eliminar_producto(index):
        productos_temp.pop(index)
        reconstruir_ticket()
        actualizar_total_temp()
        page.update()

    def autocompletar_precio(e):
        nombre_producto = producto.value.strip()
        for p in productos_db:
            if p["nombre"] == nombre_producto:
                precio.value = str(p["precio"])
                unidad_actual.value = p.get("unidad", "")
                page.update()
                return

    def filtrar_productos(e):
        texto = producto.value.lower().strip()
        sugerencias_productos.controls.clear()
        if texto == "":
            page.update()
            return
        for p in productos_db:
            if texto in p["nombre"].lower():
                sugerencias_productos.controls.append(
                    ft.TextButton(
                        content=ft.Text(p["nombre"]),
                        on_click=lambda e, prod=p: seleccionar_producto(prod)
                    )
                )
        page.update()

    def seleccionar_producto(prod):
        producto.value = prod["nombre"]
        precio.value = str(prod["precio"])
        # Capturamos la unidad del producto que viene de la consulta del controlador
        unidad_actual.value = prod.get("unidad", "")
        sugerencias_productos.controls.clear()
        page.update()

    def agregar_producto(e):
            if (
                producto.value.strip() == ""
                or precio.value.strip() == ""
                or cantidad.value.strip() == ""
            ):
                return
            
            # --- CORREGIDO: Evitar que truene si escriben letras en cantidad ---
            try:
                amount_solicitada = int(cantidad.value)
                if amount_solicitada <= 0:
                    raise ValueError
            except ValueError:
                page.snack_bar = ft.SnackBar(
                    ft.Text("⚠️ La cantidad debe ser un número entero mayor a 0")
                )
                page.snack_bar.open = True
                page.update()
                return # Detenemos la ejecución para que no intente agregar nada
            
            precio_producto = None
            stock_disponible = 0
            unidad_prod = unidad_actual.value 

            for p in productos_db:
                if p["nombre"] == producto.value:
                    precio_producto = float(p.get("precio", 0))
                    stock_disponible = int(p.get("stock", p.get("cantidad", 0)))
                    if not unidad_prod:
                        unidad_prod = p.get("unidad", "")
                    break
                    
            if precio_producto is None:
                return
            
            if amount_solicitada > stock_disponible:
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Solo hay {stock_disponible} unidades disponibles")
                )
                page.snack_bar.open = True
                page.update()
                return

            nuevo = {
                "nombre": producto.value.strip(),
                "precio": precio_producto,
                "cantidad": amount_solicitada,
                "unidad": unidad_prod 
            }

            productos_temp.append(nuevo)
            reconstruir_ticket()

            producto.value = ""
            precio.value = ""
            cantidad.value = ""
            unidad_actual.value = "" 

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
        cliente.value = "Publico en general"
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
        value="Publico en general",
        border_radius=10,
        filled=True
    )

    producto = ft.TextField(
        label="Producto",
        border_radius=10,
        filled=True,
        on_change=filtrar_productos
    )

    # --- CORREGIDO: Bloqueado, fondo gris de bloqueo y texto oscuro de alta legibilidad ---
    precio = ft.TextField(
        label="Precio",
        border_radius=10,
        filled=True,
        read_only=True,
        bgcolor="#E5E7EB", 
        color="#111827"    
    )

    cantidad = ft.TextField(
        label="Cantidad",
        border_radius=10,
        filled=True,
        hint_text="Solo números enteros",
        on_submit=agregar_producto
    )

    # Control auxiliar invisible para retener temporalmente la unidad seleccionada
    unidad_actual = ft.Text(visible=False)

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
                sugerencias_productos,
                precio,
                cantidad,
                unidad_actual, 
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

    ticket_actual = ft.Card(
        width=350,  
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Ticket Actual",
                        size=18,
                        weight="bold",
                        color=PRIMARIO
                    ),
                    ft.Row(
                        [
                            ft.Text("Producto", size=11, weight="bold", color=GRIS, expand=True),
                            ft.Text("Precio", size=11, weight="bold", color=GRIS, width=55, text_align="right"),
                            ft.Text("Cant.", size=11, weight="bold", color=GRIS, width=60, text_align="center"), 
                            ft.Text("Total", size=11, weight="bold", color=GRIS, width=65, text_align="right"),
                            ft.Container(width=40) 
                        ],
                        spacing=5
                    ),
                    ft.Divider(height=1, color="#E5E7EB"), 
                    lista_productos_temp,
                    ft.Divider(height=1, color="#E5E7EB"),
                    total_temp 
                ]
            ),
            padding=20
        )
    )

    apartado_ticket = ft.Column(
        [
            ticket_actual,
            ft.Container(
                content=total_temp,
                alignment=ft.Alignment(1.0, 0.0), 
                padding=ft.padding.only(right=10, top=15)
            )
        ],
        spacing=10
    )

    lista_ventas = ft.Card(
        expand=True,
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Historial de ventas",
                        size=18,
                        weight="bold",
                        color=PRIMARIO
                    ),
                    lista
                ],
                expand=True
            ),
            padding=20
        )
    )

    actualizar_lista()
    actualizar_total_temp()

    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    return ft.Container(
        bgcolor=FONDO,
        expand=True,
        padding=20,
        content=ft.Column([
            ft.Row(
                [
                    ft.Text(
                        "Ventas",
                        size=30,
                        weight="bold",
                        color=PRIMARIO
                    ),
                    ft.Text(
                        f"Fecha: {fecha_hoy}",
                        size=16,
                        weight="w500",
                        color=GRIS
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Row(
                [
                    formulario,
                    ticket_actual,
                    lista_ventas 
                ],
                spacing=20,
                expand=True 
            )
        ])
    )

