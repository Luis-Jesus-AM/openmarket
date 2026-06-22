import flet as ft
from controller.registro_controller import registrar_nuevo_usuario

def vista_registro(page: ft.Page):
    VERDE = "#16A34A"
    FONDO = "#F5F7FA"
    GRIS = "#6B7280"
    BLANCO = "#FFFFFF"

    input_nombre = ft.TextField(label="Nombre Completo", border_radius=10, filled=True, icon=ft.Icons.PERSON)
    input_correo = ft.TextField(label="Correo Electrónico", border_radius=10, filled=True, icon=ft.Icons.EMAIL, keyboard_type=ft.KeyboardType.EMAIL)
    input_telefono = ft.TextField(label="Teléfono (Opcional)", border_radius=10, filled=True, icon=ft.Icons.PHONE, keyboard_type=ft.KeyboardType.PHONE)
    input_pass = ft.TextField(label="Contraseña", border_radius=10, filled=True, password=True, can_reveal_password=True, icon=ft.Icons.LOCK)
    input_confirmar = ft.TextField(label="Confirmar Contraseña", border_radius=10, filled=True, password=True, can_reveal_password=True, icon=ft.Icons.LOCK_CLOCK)

    txt_mensaje = ft.Text("", size=14, weight="bold", text_align="center")

    def ejecutar_registro(e):
        resultado = registrar_nuevo_usuario(
            nombre=input_nombre.value,
            correo=input_correo.value,
            contraseña=input_pass.value,
            confirmar_contraseña=input_confirmar.value,
            telefono=input_telefono.value
        )
        if resultado["exito"]:
            txt_mensaje.value = resultado["mensaje"]
            txt_mensaje.color = "green"
            input_nombre.value = ""
            input_correo.value = ""
            input_telefono.value = ""
            input_pass.value = ""
            input_confirmar.value = ""
            page.snack_bar = ft.SnackBar(ft.Text(resultado["mensaje"]), bgcolor="green")
            page.snack_bar.open = True
        else:
            txt_mensaje.value = resultado["mensaje"]
            txt_mensaje.color = "red"
        page.update()

    def volver_al_login(e):
        from view.login_view import vista_login 
        page.clean()
        page.add(vista_login(page))
        page.update()

    btn_registrar = ft.ElevatedButton(
        "Registrar Usuario",
        bgcolor=VERDE,
        color="white",
        height=45,
        width=300,
        on_click=ejecutar_registro
    )

    btn_volver = ft.TextButton(
        "¿Ya tienes cuenta? Inicia sesión",
        style=ft.ButtonStyle(color=VERDE),
        on_click=volver_al_login 
    )

    formulario_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Registrar Nuevo Personal", size=22, weight="bold", color=VERDE, text_align="center"),
                    ft.Text("Crea cuentas para los empleados del sistema", size=12, color=GRIS, text_align="center"),
                    ft.Divider(height=15, color="#E5E7EB"),
                    input_nombre,
                    input_correo,
                    input_telefono,
                    input_pass,
                    input_confirmar,
                    txt_mensaje,
                    ft.Container(content=btn_registrar, alignment=ft.Alignment(0, 0), padding=ft.padding.only(top=10)),
                    btn_volver 
                ],
                spacing=12,
                horizontal_alignment="stretch"
            ),
            padding=25,
            width=400,
        )
    )

    return ft.Container(
        bgcolor=FONDO,
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            [formulario_card],
            alignment="center",
            horizontal_alignment="center"
        )
    )