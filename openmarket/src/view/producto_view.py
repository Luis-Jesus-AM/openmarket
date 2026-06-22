import flet as ft
from controller.producto_controller import (
    registrar_producto,
    listar_productos
)


def vista_productos(page: ft.Page):
    AZUL = "#2563EB"
    FONDO = "#F5F7FA"
    GRIS = "#6B7280"
    lista = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=False
    )

    busqueda = ft.TextField(
        label="Buscar producto",
        prefix_icon=ft.Icons.SEARCH,
        filled=True,
        border_radius=10,
        on_change=lambda e: actualizar_lista()
    )


    def actualizar_lista():
        lista.controls.clear()
        texto = busqueda.value.strip() if busqueda.value else ""
        productos = listar_productos(texto)
        productos_bajos = []

        for p in productos:
            if p["cantidad"] <= 10:
                productos_bajos.append(p["nombre"])

            lista.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.Column([
                                    ft.Text(p["nombre"], weight="bold"),
                                    ft.Text(f"Precio: ${p['precio']}", size=12, color=GRIS),
                                    ft.Text(f"Contenido: {p['descripcion'] if p['descripcion'] else 'Sin especificar'}", size=12, color=GRIS),
                                    ft.Text(
                                        f"Cantidad: {p['cantidad']}",
                                        size=12,
                                        color=(
                                            "red" if p["cantidad"] <= 15
                                            else "orange" if p["cantidad"] <= 25
                                            else GRIS
                                        )
                                    ),
                                    ft.Text(f"Unidad: {p['unidad']}", size=12, color=GRIS)
                                ]),
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                        icon_color="green",
                                        tooltip="Surtir más stock",
                                        on_click=lambda e, prod=p: abrir_modal_reabastecer(prod)
                                    ),
                                    ft.Icon(
                                        ft.Icons.INVENTORY_2,
                                        color=AZUL
                                    )
                                ], spacing=5)
                            ],
                            alignment="spaceBetween"
                        ),
                        padding=15
                    )
                )
            )

        if productos_bajos:
            page.dialog = ft.AlertDialog(
                title=ft.Text("¡Alerta de Stock!"),
                content=ft.Text(
                    "⚠ Productos por agotarse:\n\n" +
                    "\n".join(productos_bajos)
                )
            )
            page.dialog.open = True
            
        page.update()


    def abrir_modal_reabastecer(producto):
        nombre.value = producto["nombre"]
        precio.value = str(producto["precio"])
        unidad.value = producto["unidad"]
        descripcion.value = producto["descripcion"]
        cantidad.value = "" 
        page.update()

    # 👇 NUEVA FUNCIÓN: Validar en tiempo real mientras escribe
    def validar_cantidad_tiempo_real(e):
        valor = e.control.value
        
        # Si está vacío, quitar errores
        if not valor:
            e.control.error_text = None
            e.control.border_color = None
            e.control.update()
            return
        
        # Si tiene letras o caracteres no válidos
        if not valor.isdigit():
            e.control.error_text = "⚠️ Solo números enteros"
            e.control.border_color = ft.Colors.RED_400
            e.control.update()
        else:
            e.control.error_text = None
            e.control.border_color = None
            e.control.update()

        
    def agregar_producto(e):
        # 🛑 Validar que cantidad sea solo números enteros positivos
        cantidad_valor = cantidad.value.strip()
        
        # Validar si está vacío
        if not cantidad_valor:
            cantidad.error_text = "Este campo es obligatorio"
            cantidad.border_color = ft.Colors.RED_400
            page.snack_bar = ft.SnackBar(
                ft.Text("❌ Error: Debes ingresar una cantidad", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_400,
                duration=3000
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # Validar que sean solo números
        if not cantidad_valor.isdigit():
            cantidad.error_text = "⚠️ Solo números enteros"
            cantidad.border_color = ft.Colors.RED_400
            page.snack_bar = ft.SnackBar(
                ft.Text("❌ Error: La cantidad debe ser un número entero (sin letras ni decimales)", 
                    color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_400,
                duration=3000
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # Convertir a entero
        cantidad_int = int(cantidad_valor)
        
        # Validar que no sea cero o negativo
        if cantidad_int <= 0:
            cantidad.error_text = "Debe ser mayor a 0"
            cantidad.border_color = ft.Colors.RED_400
            page.snack_bar = ft.SnackBar(
                ft.Text("❌ Error: La cantidad debe ser mayor a 0", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_400,
                duration=3000
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # Quitar errores si todo está bien
        cantidad.error_text = None
        cantidad.border_color = None
        
        # 🛑 Validar que precio sea número válido
        try:
            precio_float = float(precio.value.strip())
            if precio_float < 0:
                raise ValueError
        except ValueError:
            precio.error_text = "Ingrese un precio válido"
            precio.border_color = ft.Colors.RED_400
            page.snack_bar = ft.SnackBar(
                ft.Text("❌ Error: El precio debe ser un número válido", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_400,
                duration=3000
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # Quitar error de precio si pasó
        precio.error_text = None
        precio.border_color = None

        # Mandamos los argumentos a tu controlador
        registrado = registrar_producto(
            nombre.value,
            descripcion.value,
            precio.value,
            str(cantidad_int),
            "General",
            1,
            unidad.value,
        )

        if not registrado:
            page.snack_bar = ft.SnackBar(
                ft.Text("❌ Error al registrar el producto", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_400
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # Limpieza de campos
        nombre.value = ""
        precio.value = ""
        cantidad.value = ""
        unidad.value = ""
        descripcion.value = ""
        
        # Limpiar errores visuales
        cantidad.error_text = None
        cantidad.border_color = None
        precio.error_text = None
        precio.border_color = None

        actualizar_lista()
        
        # ✅ Mensaje de éxito
        page.snack_bar = ft.SnackBar(
            ft.Text("✅ Producto agregado exitosamente", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN_400
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

    # 👇 CAMPO CORREGIDO: Sin keyboard_type NUMBER para permitir validación
    cantidad = ft.TextField(
        label="Cantidad (solo números)",
        border_radius=10,
        filled=True,
        hint_text="Ej: 10",
        on_change=validar_cantidad_tiempo_real  # 👈 Valida en tiempo real
    )

    unidad = ft.TextField(
        label="Unidad de medida",
        border_radius=10,
        filled=True
    )
    
    descripcion = ft.TextField(
        label="Contenido / Descripción (ej: Caja con 12 pzs)",
        border_radius=10,
        filled=True
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
                cantidad,
                unidad,
                descripcion,
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
        expand=True,
        content=ft.Container(
            content=ft.Column([
                ft.Text(
                    "Productos registrados",
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